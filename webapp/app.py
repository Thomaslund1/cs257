import argparse
import flask
import api


app = flask.Flask(__name__)
@app.route('/')
@app.route('/home')
def home():
    return flask.render_template('index.html')


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
    args = flask.request.args.getlist()
    print(args)
    return flask.render_template('games.html')

@app.route('/game')
def returnGame():

    return flask.render_template('game.html')

@app.route('/recommender')
def returnRecommender():
    return flask.render_template('topGames.html')

@app.route('/users')
def returnUsers():
    return flask.render_template('users.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
