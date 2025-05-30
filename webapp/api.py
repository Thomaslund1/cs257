import psycopg2 as psy
from flask import Flask, jsonify
import sys
import config

app = Flask(__name__)


def get_connection():
    ''' Returns a database connection object with which you can create cursors,
        issue SQL queries, etc. This function is extremely aggressive about
        failed connections--it just prints an error message and kills the whole
        program. Sometimes that's the right choice, but it depends on your
        error-handling needs. '''
    try:
        return psy.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

def getAllMechanics():
    query = 'SELECT id, mechanics FROM mechanics ORDER BY mechanics'
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    return [(row[0], row[1]) for row in cursor]


def getId(id):
    out = []
    try:
        query = '''
            SELECT * 
            FROM game WHERE game.id = %s
        '''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (id,))
        for row in cursor:
            out.append(row)
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    print(query)
    if out == []:
        out = 'No results found'
    return jsonify({'name': out})

def queryGames(params):
    out = []
    joins = ["name"]
    wheres = []
    values = []

    # Handle special 'plays' case (which involves min and max)
    if 'plays' in params:
        min_plays = params.get('minPlays', 0)
        max_plays = params.get('maxPlays', 10000)

        joins.extend([
            "minplays AS minplays_table",
            "minplays_to_name AS minplays_map",
            "maxplays AS maxplays_table",
            "maxplays_to_name AS maxplays_map"
        ])
        wheres.extend([
            "minplays_table.value >= %s",
            "maxplays_table.value <= %s",
            "minplays_table.id = minplays_map.minplays_to_nameId",
            "maxplays_table.id = maxplays_map.maxplays_to_nameId",
            "name.id = minplays_map.nameid",
            "name.id = maxplays_map.nameid"
        ])
        values.extend([min_plays, max_plays])

    # Handle minage (age filter)
    if 'age' in params:
        joins.append("minage AS minage_table")
        joins.append("minage_to_name AS minage_map")
        wheres.extend([
            "minage_table.value <= %s",
            "minage_table.id = minage_map.minage_to_nameId",
            "name.id = minage_map.nameid"
        ])
        values.append(params['age'])

    # Handle time (playtime filter)
    if 'time' in params:
        joins.append("minplaytime AS minplaytime_table")
        joins.append("minplaytime_to_name AS minplaytime_map")
        wheres.extend([
            "minplaytime_table.value <= %s",
            "minplaytime_table.id = minplaytime_map.minplaytime_to_nameId",
            "name.id = minplaytime_map.nameid"
        ])
        values.append(params['time'])

    # Headers to include (excluding special keys)
    valid_headers = ['artist', 'designer', 'maxplayers', 'minplayers', 'minplaytime',
                     'name', 'complexity', 'minage', 'maxplaytime', 'mechanics']
    special_keys = ['plays', 'age', 'time']

    for i, (header, searchTerm) in enumerate(params.items()):
        if header in special_keys:
            continue  # already processed
        if header not in valid_headers:
            return None  # invalid key

        alias = f"{header}_{i}"
        joins.append(f"{header} AS {alias}")
        joins.append(f"{header}_to_name AS {alias}_map")

        # Filter
        wheres.append(f"{alias}.{header} ILIKE %s")
        values.append(f"%{searchTerm}%")

        # Join conditions
        wheres.append(f"{alias}.id = {alias}_map.{header}_to_nameId")
        wheres.append(f"name.id = {alias}_map.nameid")

    # Build query
    query = f"SELECT DISTINCT name.name FROM {', '.join(joins)}"
    if wheres:
        query += f" WHERE {' AND '.join(wheres)}"
    query += ";"

    # Execute
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
        out = [row[0] for row in cursor]
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
        return None

    return out




def getNames(searchTerm='%'):
    out = []
    try:
        query = f'''
            SELECT * 
            FROM name
            WHERE name.name LIKE %s;
        '''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (f'{searchTerm}%',))
        for row in cursor:
            out.append(row)
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    if out == []:
        out = 'No results found'
    return jsonify({'name': out})

def queryGamesNames(header,searchTerm):
    out = []
    try:
        valid_headers = ['artist','designer','maxplayers','minplayers','minplaytime','name']
        if header not in valid_headers:
            return "That is not a recognized paramater, check spelling/caps"
        query = f'''
            SELECT * 
            FROM name, {header}, {header}_to_name
            WHERE {header}.{header} LIKE %s
            AND {header}.id = {header}_to_name.{header}_to_nameId
            AND name.id = {header}_to_name.nameid;
        '''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (f'%{searchTerm}%',)) 
        for row in cursor:
            out.append(row[0])
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    if out == []:
        out = 'No results found'
    return jsonify({'name': out})

@app.route('/api/search_games')
def search_games():
    query = Flask.request.args.get('q', '').strip()
    out = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        if query.lower() == "all":
            cursor.execute(
                "SELECT id, name, yearpublished, average, playingtime, age, minplayers, maxplayers, designer FROM game ORDER BY average DESC LIMIT 100"
            )
        elif len(query) >= 3:
            cursor.execute(
                "SELECT id, name, yearpublished, average, playingtime, age, minplayers, maxplayers, designer FROM game WHERE name ILIKE %s ORDER BY average DESC LIMIT 10",
                (f"%{query}%",)
            )
        else:
            return Flask.jsonify(results=[])
        for row in cursor.fetchall():
            out.append({
                "id": row[0],
                "name": row[1],
                "yearpublished": row[2],
                "average": row[3],
                "playingtime": row[4],
                "age": row[5],
                "minplayers": row[6],
                "maxplayers": row[7],
                "designer": row[8]
            })
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    return Flask.jsonify(results=out)


@app.route('/api/game_names')
def game_names():
    out = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM name ORDER BY name ASC;")
        for row in cursor:
            out.append(row[0])
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    return jsonify(out)


def getFromArgs(args):
    return