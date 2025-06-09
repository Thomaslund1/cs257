import psycopg2
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
    query = 'SELECT id, mechanics FROM mechanics'
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
    #Buckle up, this is as much cursed SQL as I could cobble together in a few short weeks
    """
    A function that creates and executes the final SQL command for data retreival 
    @param params(lol) : dict 
          - The list of search terms and their field from the url
    @returns out
          - A list of games output from the search function
    """
    out = []
    joins = ["name"]
    wheres = []
    values = []

    # a few search terms are 'special' because they need to be searched for differently
    #Here plays is an int that needs to be within min and max of each game that gets returned
    #is this the most efficent term to start with? almost certainly not
    if 'plays' in params:
        plays = params.get('plays')

        joins.extend([
            "minplayers AS minplayers_table",
            "minplayers_to_name AS minplayers_map",
            "maxplayers AS maxplayers_table",
            "maxplayers_to_name AS maxplayers_map"
        ])
        wheres.extend([
            "CAST(minplayers_table.minplayers AS INTEGER) <= %s",
            "CAST(maxplayers_table.maxplayers AS INTEGER) >= %s",
            "minplayers_table.id = minplayers_map.minplayers_to_nameid",
            "maxplayers_table.id = maxplayers_map.maxplayers_to_nameid",
            "name.id = minplayers_map.nameid",
            "name.id = maxplayers_map.nameid"
        ])
        values.extend([plays, plays])

    #similarly minimum player age needs to be less than the age given
    if 'age' in params:
        joins.append("age AS age_table")
        joins.append("age_to_name AS age_map")
        wheres.extend([
            "CAST(age_table.age AS INTEGER) <= %s",
            "age_table.id = age_map.age_to_nameid",
            "name.id = age_map.nameid"
        ])
        values.append(params['age'])

   #Time should also be less
    if 'time' in params:
        joins.append("minplaytime AS minplaytime_table")
        joins.append("minplaytime_to_name AS minplaytime_map")
        wheres.extend([
            "CAST(minplaytime_table.minplaytime AS INTEGER) <= %s",
            "CAST(minplaytime_table.minplaytime AS INTEGER) > 0",
            "minplaytime_table.id = minplaytime_map.minplaytime_to_nameid",
            "name.id = minplaytime_map.nameid"
        ])
        values.append(params['time'])

    #mechanics are fun... 
    #They get pulled from a special sql dt 
    mechanics_ids = params.get('mechanics', [])
    mechanics_count = len(mechanics_ids)
    if mechanics_count > 0:
        joins.append("mechanics_to_name AS mechanics_map")
        wheres.append("mechanics_map.nameid = name.id")
        wheres.append(f"mechanics_map.mechanics_to_nameid IN ({','.join(['%s'] * mechanics_count)})")
        values.extend(mechanics_ids)
    #10/10 sql sanitizaton
    valid_headers = [
        'artist', 'designer', 'maxplayers', 'minplayers', 'minplaytime',
        'name', 'complexity', 'age', 'maxplaytime', 'mechanics'
    ]
    #ignore these in the loop
    special_keys = ['plays', 'age', 'time', 'mechanics']

    #with the paramater.id, paramater_to_names, and names.id we have 
    #to do some schenanigans to make the search work
    #I present schenanigans:
    for i, (header, searchTerm) in enumerate(params.items()):
        if header in special_keys:
            continue  

        if header not in valid_headers:
            return None  # invalid key

        if header == 'name':
            wheres.append("name.name ILIKE %s")
            values.append(f"%{searchTerm}%")
            continue

        alias = f"{header}_{i}"
        map_alias = f"{alias}_map"

        joins.append(f"{header} AS {alias}")
        joins.append(f"{header}_to_name AS {map_alias}")

        
        if header in ['artist', 'designer']:
            wheres.append(f"{alias}.{header} ILIKE %s")
            values.append(f"%{searchTerm}%")
        else:
            wheres.append(f"{alias}.{header} = %s")
            values.append(searchTerm)

        wheres.append(f"{alias}.id = {map_alias}.{header}_to_nameid")
        wheres.append(f"name.id = {map_alias}.nameid")

   
    query = f"SELECT DISTINCT name.name FROM {', '.join(joins)}"
    if wheres:
        query += f" WHERE {' AND '.join(wheres)}"
    query += ";"

    # Run the query
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
    
    #schenanefoolery of adding ratings sorting because I don't know how to add a sort by paramater to this mess
    rates = []
    names = tuple(out)  

    if names:
        query = """
        SELECT name.name, rating.rating
        FROM name
        JOIN rating_to_name ON name.id = rating_to_name.nameid
        JOIN rating ON rating.id = rating_to_name.rating_to_nameid
        WHERE name.name IN %s;
        """

    connection = get_connection()  
    cursor = connection.cursor()
    cursor.execute(query, (names,))  
    ratings_dict = {}
    for name, rating in cursor:
        if name not in ratings_dict:
            ratings_dict[name] = []
            ratings_dict[name].append(str(rating)) 

    for name in out:
        rates.append(ratings_dict.get(name, [])) 
    cursor.close()
    connection.close()
    print("All ratings:", rates)
    flat_ratings = [rate[0] for rate in rates]

    combined = list(zip(out, flat_ratings))

    sorted_combined = sorted(combined, key=lambda x: x[1], reverse=True)

    sorted_out, sorted_ratings = zip(*sorted_combined)

    sorted_out = list(sorted_out)
    sorted_ratings = list(sorted_ratings)

    print("Sorted Game Names:", sorted_out)
    print("Sorted Ratings:", sorted_ratings)
    return sorted_out

def getParams(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM game WHERE game.name=%s',(id,))
    headers = "id,name,designer,publisher,artist,yearpublished,minplayers,maxplayers,playingtime,minplaytime,maxplaytime,age,usersrated,average,bayesaverage,rank,rank_wg,numcomments,numweights,averageweight,stddev,median,owned,trading,wanting,wishing,userrating,image,category,mechanic,comment,1player,2player,3player,4player,5player,6player,7player,8player,9player,10player,11player,12player,13player,14player,15player,16player,17player,18player,19player,20player,description,exp,basegame,basegame_name,reimplement,reimplement_name,reimplemented,reimplemented_name,contains,contains_name,iscontained,iscontained_name,integration,integration_name,accessories,accessories_name,numplays,price,userweight,wishpriority,expansions,domain,family,age_poll,name_others,comments_GL,thumbs_GL,sold_GL,price_GL,currency_GL,user_GL,tags,tags_user"
    headers = headers.split(',')
    return [row for row in cursor],headers
def getFromArgs(args):
    return