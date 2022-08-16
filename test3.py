from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import json
from ranker import GameRank
print("Starting")

test3 = Flask(__name__)
test3.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ranking.db'
test3.config['SQLALCHEMY_BINDS'] = {
    'db1': 'sqlite:///ranking.db',
}
test3.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(test3)

def getRank():
    with open("data/index.json") as f:
        games = json.load(f)
    with open("data/indexList.json") as f:
        gameList = json.load(f)
    with open("data/wordBank.json") as f:
        wordBank = json.load(f)
#textBank = pickle.load(open("data/textBank.pkl", 'rb'))
    return GameRank(games, gameList, wordBank)
ranks = []
class Ranking(db.Model):
    __bind_key__ = 'db1'
    id = db.Column(db.Integer, primary_key=True)
    que = db.Column(db.String(200), nullable=False)
    rank = db.Column(db.PickleType, default=[])

    def __repr__(self):
        return '<Query %r>' % self.id

#class Ranks()

@test3.before_first_request
def do_something_only_once():
    global ranks
    ranks = getRank()

@test3.route('/', methods=['POST', 'GET'])
def index():
    query = Ranking.query.one_or_none()
    if request.method == 'POST':
        print("pos")
        global ranks
        if query:
            print("query")
            
            query.que = request.form['content']
            if not query or query.que == '':
                query.rank = []
            elif ranks.query_bool(query.que):
                query.rank = ranks.get_rank(ranks.querier(query.que))
            else:
                query.rank = ranks.get_rank(ranks.rank1(query.que))
            
            try:
                db.session.commit()
                return redirect('/')
            except:
                return "There was an issue fetching the games"
        else:
            print("no query")
            query = request.form['content']
            newRank = []
            if not query or query == '':
                pass;
            elif ranks.query_bool(query):
                newRank = ranks.get_rank(ranks.querier(query))
            else:
                newRank = ranks.get_rank(ranks.rank1(query))
            new_query = Ranking(que=query, rank=newRank)
            try:
                db.session.add(new_query)
                db.session.commit()
                return redirect('/')
            except:
                return "There was an issue fetching the games"
    else:
        if query:
            print("Ayo")
            return render_template('index.html', ranks=query)
        return render_template('index.html', ranks=[])

if __name__ == "__main__":
    test3.run(debug=True)
