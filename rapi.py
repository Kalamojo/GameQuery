from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from ranker import GameRank
import json

rapi = Flask(__name__)
rapi.config['SQLALCHEMY_BINDS'] = {
    'db1': 'sqlite:///ranks2.db',
    'db3': 'sqlite:///index.db'
}
rapi.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(rapi)

class Rank(db.Model):
    __bind_key__ = 'db1'
    id = db.Column(db.Integer, primary_key=True)
    gameList = db.Column(db.PickleType, nullable=False)
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
    rank = Rank.query.one_or_none()
    index = Index.query.one_or_none()
    ranks = GameRank(index.games, rank.gameList)

@rapi.route('/', methods=['GET'])
def home():
    """
    new_Rank = Rank(gameList=json.load(open("indexList.json")))
    db.session.add(new_Rank)
    db.session.commit()
    """
    return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.1/css/bulma.min.css" />
            <title>RAPI</title>
        </head>
        <body>
            <section class="hero is-success">
                <div class="hero-body has-text-centered">
                    <h1 class="title">RAPI</h1>
                    <h1 class="subtitle">Ranking API for GameQuery</h1>
                </div>
            </section>
        </body>
        </html>
    """

@rapi.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@rapi.route('/api/rank', methods=['GET'])
def qToRank():
    query_parameters = request.args
    query = query_parameters.get('query')
    print(query)
    if not query:
        return page_not_found(404)
    global ranks
    return jsonify(ranks.queryToRank(query))


if __name__ == "__main__":
    rapi.run(debug=True)