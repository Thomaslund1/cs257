import flask as fl
import psycopg2 as psy
import argparse as ap
import sys
import config

app = fl.Flask(__name__)

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
    return out

def queryGames(header,searchTerm):
    
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
            out.append([row[0],row[2]])
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    if out == []:
        out = 'No results found'
    return out

@app.route('/games/name/<searchTerm>')
@app.route('/games/name/')
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
        print(query)
    except Exception as e:
        print(e, file=sys.stderr)
    if out == []:
        out = 'No results found'
    return out


@app.route('/games/<paramater>/<searchTerm>')
@app.route('/games/<paramater>')
def funt(paramater,searchTerm='%'):
    return queryGames(paramater,searchTerm)


@app.route('/game/<id>')
def id(id):
    return getId(id)

@app.route('/games')
def lotsaMotsa():
    return "Whoa, thats a lot of data, try adding one of these search paramaters: designer, artist, " \
    "minplayers, minplaytime"



@app.route('/help')
def get_help():
    return fl.render_template('help.html')

@app.route('/')
def homepage():
    return 'This is the homepage, \n neat right? Check out our help page at /help, or \n try running "//games//artist//A" to get all games whose name starts with A'

if __name__ == '__main__':
    parser = ap.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)