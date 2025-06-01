import argparse
import flask
import api
import sys
import config
import psycopg2


app = flask.Flask(__name__)

def get_connection():
    try:
        return psycopg2.connect(
            database=config.database,
            user=config.user,
            password=config.password,
            host=getattr(config, 'host', 'localhost'),
            port=getattr(config, 'port', 5432)
        )
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

@app.route('/')
@app.route('/home')
def home():
    return flask.render_template('index.html')

@app.route('/api/game_names')
def game_names():
    return api.game_names()

@app.route('/api/mechanics')
def returnMechanics():
    mechanics = api.getAllMechanics()
    return flask.jsonify([{"id": m_id, "name": m_name} for m_id, m_name in mechanics])



@app.route('/api/name/<searchTerm>')
@app.route('/api/name/')
def returnName(searchTerm):
    return api.getNames(searchTerm)

@app.route('/search')
def search():
    query = flask.request.args.get('q', '').strip()
    return flask.render_template('search.html', query=query)

@app.route('/games')
def returnGames():
    args = flask.request.args
    print(args)
    sortedVals = api.queryGames(args)
    listBody = ''
    print(sortedVals)
    if sortedVals == None:
        return flask.render_template('searchResults.html', listBody = 'No results found')
    for i in sortedVals:
        listBody += (f'<li>{i}</li>\n')
    return flask.render_template('searchResults.html', listBody = listBody)

@app.route('/game/<id>')
def returnGame(id):
    params,headers = api.getParams(id)
    return flask.render_template('game.html',params=params[0], headers=headers)

@app.route('/recommender')
def returnRecommender():
    return flask.render_template('recommender.html')

@app.route('/users')
def returnUsers():
    return flask.render_template('users.html')

app.route('/api/search_games')
def search_games():
    query = flask.request.args.get('q', '').strip()
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
            return flask.jsonify(results=[])
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
    print(out)
    return flask.jsonify(results=out)

@app.route('/search_results')
def search_results():
    query = flask.request.args.get('q', '').strip()
    return flask.render_template('search_results.html', query=query)

@app.route('/game/<game_name>')
def game_detail(game_name):
    # Fetch game data from the database using the name
    connection = api.get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM game WHERE name = %s LIMIT 1;", (game_name,)
    )
    row = cursor.fetchone()
    connection.close()
    if row:
        # Adjust the keys to match your table columns
        columns = [desc[0] for desc in cursor.description]
        game_data = dict(zip(columns, row))
        return flask.render_template('game.html', game=game_data)
    else:
        return flask.render_template('game.html', game=None)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
