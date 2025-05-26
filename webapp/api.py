import psycopg2 as psy
from flask import jsonify
import sys
import config


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
    try:
        valid_headers = ['artist', 'designer', 'maxplayers', 'minplayers', 'minplaytime',
                         'name', 'complexity', 'minage', 'maxplaytime', 'mechanics']

        joins = []
        wheres = []
        values = []

        for i, (header, searchTerm) in enumerate(params.items()):
            if header not in valid_headers:
                return None  # invalid parameter key

            alias = f"{header}_{i}"
            joins.append(f"{header} AS {alias}")
            joins.append(f"{header}_to_name AS {alias}_map")

            # Use ILIKE for case-insensitive partial matching
            wheres.append(f"{alias}.{header} ILIKE %s")
            values.append(f"%{searchTerm}%")

            wheres.append(f"{alias}.id = {alias}_map.{header}_to_nameId")
            wheres.append(f"name.id = {alias}_map.nameid")

        joins.insert(0, "name")

        query = f"SELECT DISTINCT name.name FROM {', '.join(joins)}"
        if wheres:
            query += f" WHERE {' AND '.join(wheres)}"
        query += ";"

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, values)
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

def getFromArgs(args):
    return