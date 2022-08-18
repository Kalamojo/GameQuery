from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from ranker import GameRank

rapi = Flask(__name__)
rapi.config['SQLALCHEMY_BINDS'] = {
    'db1': 'sqlite:///ranking.db',
    'db2': 'sqlite:///ranks.db',
    'db3': 'sqlite:///index.db'
}
rapi.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(rapi)

class Ranking(db.Model):
    __bind_key__ = 'db1'
    id = db.Column(db.Integer, primary_key=True)
    que = db.Column(db.String(200), nullable=False)
    rank = db.Column(db.PickleType, default=[])
    def __repr__(self):
        return '<Query %r>' % self.id

class Ranks(db.Model):
    __bind_key__ = 'db2'
    id = db.Column(db.Integer, primary_key=True)
    gameList = db.Column(db.PickleType, nullable=False)
    wordBank = db.Column(db.PickleType, nullable=False)
    def __repr__(self):
        return '<Rank %r>' % self.id

class Index(db.Model):
    __bind_key__ = 'db3'
    id = db.Column(db.Integer, primary_key=True)
    games = db.Column(db.PickleType, nullable=False)
    def __repr__(self):
        return '<Index %r>' % self.id

ranks = []

@rapi.before_first_request
def do_something_only_once():
    global ranks
    rank = Ranks.query.one_or_none()
    index = Index.query.one_or_none()
    ranks = GameRank(index.games, rank.gameList, rank.wordBank)

@rapi.route('/', methods=['GET'])
def home():
    return render_template('api.html')

@rapi.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@rapi.route('/api/v1/rank', methods=['GET'])
def qToRank():
    query_parameters = request.args
    query = query_parameters.get('query')
    if not query:
        return page_not_found(404)
    global ranks
    return jsonify(ranks.queryToRank(query))


if __name__ == "__main__":
    rapi.run(debug=True)