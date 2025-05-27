import argparse
import flask
import api
import sys


app = flask.Flask(__name__)
@app.route('/')
@app.route('/home')
def home():
    return flask.render_template('index.html')

@app.route('/api/mechanics')
def returnMechanics():
    return api.getAllMechanics()

@app.route('/api/<paramater>/<searchTerm>')
@app.route('/api/<paramater>')
def funt(paramater,searchTerm='%'):
    return api.queryGames(paramater,searchTerm)

@app.route('/api/name/<searchTerm>')
@app.route('/api/name/')
def returnName(searchTerm):
    return api.getNames(searchTerm)

@app.route('/search')
def land():
    return flask.render_template('mainSearchPage.html')

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

@app.route('/game')
def returnGame():
    return flask.render_template('game.html')

@app.route('/recommender')
def returnRecommender():
    return flask.render_template('topGames.html')

@app.route('/users')
def returnUsers():
    return flask.render_template('users.html')

app.route('/api/search_games')
def search_games():
    query = flask.request.args.get('q', '').strip()
    out = []
    try:
        connection = api.get_connection()
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
    return flask.jsonify(results=out)

@app.route('/search_results')
def search_results():
    query = flask.request.args.get('q', '').strip()
    return flask.render_template('search_results.html', query=query)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
