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
    query = 'SELECT DISTINCT * FROM mechanics.mechanics'
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    out = []
    for i in cursor:
        out.append(i)
    return out

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
    joins = []
    wheres = []
    values = []
    # Check if plays parameter exists, and set up minPlays and maxPlays filters
    if('plays' in params.keys()):
        min_plays = params.get('minPlays', 0)  # Default to 0 if not specified
        max_plays = params.get('maxPlays', 10000)  # Default to 10,000 if not specified
        # Joins for minplays and maxplays tables
        joins.append("minplays AS minplays_table")
        joins.append("maxplays AS maxplays_table")
        joins.append("minplays_to_name AS minplays_map")
        joins.append("maxplays_to_name AS maxplays_map")
        
        # Filters for plays range
        wheres.append(f"minplays_table.value >= {min_plays}")
        wheres.append(f"maxplays_table.value <= {max_plays}")
        wheres.append("minplays_table.id = minplays_map.minplays_to_nameId")
        wheres.append("maxplays_table.id = maxplays_map.maxplays_to_nameId")
        wheres.append("name.id = minplays_map.nameid")
        wheres.append("name.id = maxplays_map.nameid")
    
    # Check if complexity parameter exists, and set up complexity filter
    if('complexity' in params.keys()):
        complexity_range = 0.5  # Let's assume a 0.5 complexity range tolerance
        target_complexity = params['complexity']
        wheres.append(f"complexity BETWEEN {target_complexity - complexity_range} AND {target_complexity + complexity_range}")
    
    # Check if age parameter exists, and set up age filter
    if('age' in params.keys()):
        max_age = params['age']  # Assuming 'age' is the maximum acceptable age
        wheres.append(f"minage <= {max_age}")
    
    # Check if time parameter exists, and set up time filter
    if('time' in params.keys()):
        max_playtime = params['time']  # Assuming 'time' is the max acceptable playtime
        wheres.append(f"minplaytime <= {max_playtime}")
    
    try:
        # List of valid headers
        valid_headers = ['artist', 'designer', 'maxplayers', 'minplayers', 'minplaytime',
                         'name', 'complexity', 'minage', 'maxplaytime', 'mechanics']


        # Loop over params to add dynamic conditions
        for i, (header, searchTerm) in enumerate(params.items()):
            if header not in valid_headers:
                return None  # Invalid parameter key

            alias = f"{header}_{i}"
            joins.append(f"{header} AS {alias}")
            joins.append(f"{header}_to_name AS {alias}_map")

            # Use ILIKE for case-insensitive partial matching
            wheres.append(f"{alias}.{header} ILIKE %s")
            values.append(f"%{searchTerm}%")

            # Adding join conditions
            wheres.append(f"{alias}.id = {alias}_map.{header}_to_nameId")
            wheres.append(f"name.id = {alias}_map.nameid")

        # Starting query with 'name' table
        joins.insert(0, "name")

        query = f"SELECT DISTINCT name.name FROM {', '.join(joins)}"

        # Add WHERE clauses if there are any filters
        if wheres:
            query += f" WHERE {' AND '.join(wheres)}"

        query += ";"

        # Execute query
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
        
        # Collect results
        for row in cursor:
            out.append(row[0])
        
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