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


def queryGames(params):
    out = []
    joins = ["name"]
    wheres = []
    values = []

    # --- PLAYERS FILTER (using minplayers and maxplayers) ---
    if 'plays' in params:
        min_plays = params.get('minPlays', 0)
        max_plays = params.get('maxPlays', 10000)

        joins.extend([
            "minplayers AS minplayers_table",
            "minplayers_to_name AS minplayers_map",
            "maxplayers AS maxplayers_table",
            "maxplayers_to_name AS maxplayers_map"
        ])
        wheres.extend([
            "CAST(minplayers_table.minplayers AS INTEGER) >= %s",
            "CAST(maxplayers_table.maxplayers AS INTEGER) <= %s",
            "minplayers_table.id = minplayers_map.minplayers_to_nameid",
            "maxplayers_table.id = maxplayers_map.maxplayers_to_nameid",
            "name.id = minplayers_map.nameid",
            "name.id = maxplayers_map.nameid"
        ])


        values.extend([min_plays, max_plays])

    # --- AGE FILTER ---
    if 'age' in params:
        joins.append("age AS age_table")
        joins.append("age_to_name AS age_map")
        wheres.extend([
            "CAST(age_table.age AS INTEGER) <= %s",
            "age_table.id = age_map.age_to_nameid",
            "name.id = age_map.nameid"
        ])
        values.append(params['age'])

    # --- PLAYTIME FILTER ---
    if 'time' in params:
        joins.append("minplaytime AS minplaytime_table")
        joins.append("minplaytime_to_name AS minplaytime_map")
        wheres.extend([
            "CAST(minplaytime_table.minplaytime AS INTEGER) <= %s",
            "CAST(minplaytime_table.minplaytime AS INTEGER) > 0",  # exclude zero min times
            "minplaytime_table.id = minplaytime_map.minplaytime_to_nameid",
            "name.id = minplaytime_map.nameid"
        ])


        values.append(params['time'])


    # --- VALID PARAM-TO-TABLE FILTERS ---
    valid_headers = [
        'artist', 'designer', 'maxplayers', 'minplayers', 'minplaytime',
        'name', 'complexity', 'age', 'maxplaytime', 'mechanics'
    ]
    special_keys = ['plays', 'age', 'time']

    for i, (header, searchTerm) in enumerate(params.items()):
        if header == 'name':
            # Direct filter on name.name (no join)
            wheres.append("name.name ILIKE %s")
            values.append(f"%{searchTerm}%")
            continue
        if header in special_keys:
            continue
        if header not in valid_headers:
            return None  # Invalid key

        alias = f"{header}_{i}"
        map_alias = f"{alias}_map"

        joins.append(f"{header} AS {alias}")
        joins.append(f"{header}_to_name AS {map_alias}")

        # Use ILIKE for text-based fields, exact match for numeric
        if header in ['artist', 'designer', 'name', 'mechanics']:
            wheres.append(f"{alias}.{header} ILIKE %s")
            values.append(f"%{searchTerm}%")
        else:
            wheres.append(f"{alias}.{header} = %s")
            values.append(searchTerm)

        # Join logic
        wheres.append(f"{alias}.id = {map_alias}.{header}id")
        wheres.append(f"name.id = {map_alias}.nameid")

    # --- FINAL QUERY BUILD ---
    query = f"SELECT DISTINCT name.name FROM {', '.join(joins)}"
    if wheres:
        query += f" WHERE {' AND '.join(wheres)}"
    query += ";"

    # --- EXECUTE ---
    try:
        print("QUERY:", query)
        print("VALUES:", values)
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
        out = [row[0] for row in cursor]
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
        return None

    return out



def getFromArgs(args):
    return