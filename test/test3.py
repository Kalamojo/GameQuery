from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from ranker import GameRank
print("Starting")

test3 = Flask(__name__)
test3.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ranking.db'
test3.config['SQLALCHEMY_BINDS'] = {
    'db1': 'sqlite:///ranking.db',
    'db2': 'sqlite:///ranks.db',
    'db3': 'sqlite:///index.db'
}
test3.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(test3)

def getRank(a, b, c):
    return GameRank(a, b, c)
ranks = []
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
"""
@test3.before_first_request
def do_something_only_once():
    global ranks
    ranks = getRank()
"""

@test3.route('/', methods=['POST', 'GET'])
def index():
    """
    new_Rank = Ranks(gameList=json.load(open("data/indexList.json")), 
                    wordBank=json.load(open("data/wordBank.json")))
    new_Index = Index(games=json.load(open("data/index.json")))
    db.session.add(new_Index)
    db.session.add(new_Rank)
    db.session.commit()
    """
    query = Ranking.query.one_or_none()
    if request.method == 'POST':
        print("pos")
        global ranks
        if ranks == []:
            rank = Ranks.query.one_or_none()
            index = Index.query.one_or_none()
            ranks = getRank(index.games, rank.gameList, rank.wordBank)
        if query:
            print("query")
            
            query.que = request.form['content']
            query.rank = ranks.queryToRank(query.que)
            try:
                db.session.commit()
                return redirect('/')
            except:
                return "There was an issue fetching the games"
        else:
            print("no query")
            #new_Rank = Ranks(gameList=json.load(open("data/indexList.json")), 
            #                wordBank=json.load(open("data/wordBank.json")))
            #new_Index = Index(games=json.load(open("data/index.json")))
            #ranks = getRank(new_Index.games, new_Rank.gameList, new_Rank.wordBank)
            query = request.form['content']
            newRank = ranks.queryToRank(query)
            new_query = Ranking(que=query, rank=newRank)
            try:
                #db.session.add(new_Index)
                #db.session.add(new_Rank)
                db.session.add(new_query)
                db.session.commit()
                return redirect('/')
            except:
                return "There was an issue fetching the games"
    else:
        if query:
            print("Ayo")
            return render_template('index.html', ranks=query)
        
            #new_Rank = Ranks(gameList=json.load(open("data/indexList.json")), 
            #                wordBank=json.load(open("data/wordBank.json")))
            #new_Index = Index(games=json.load(open("data/index.json")))
            #db.session.add(new_Index)
            #db.session.add(new_Rank)
            #db.session.commit()
        return render_template('index.html', ranks=[])

if __name__ == "__main__":
    test3.run(debug=True)
