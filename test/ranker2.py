from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
import rankerer as rankerer

ranker2 = Flask(__name__)
ranker2.config['SQLALCHEMY_BINDS'] = {
    'db1': 'sqlite:///games.db',
    'db2': 'sqlite:///gameRepo.db',
    'db3': 'sqlite:///ranking.db',
}
ranker2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(ranker2)

ranks = []

class Gamers(db.Model):
    __bind_key__ = 'db1'
    id = db.Column(db.Integer, primary_key=True)
    ind = db.Column(db.Integer, nullable=False)
    genres = db.Column(db.PickleType, nullable=True)
    themes = db.Column(db.PickleType, nullable=True)
    name = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=False)
    def __repr__(self):
        return '<%r>' % self.name

class Repos(db.Model):
    __bind_key__ = 'db2'
    id = db.Column(db.Integer, primary_key=True)
    gameList = db.Column(db.String, nullable=False)
    wordBank = db.Column(db.PickleType, nullable=False)
    def __repr__(self):
        return '<Repo %r>' % self.id

class Ranking(db.Model):
    __bind_key__ = 'db3'
    id = db.Column(db.Integer, primary_key=True)
    que = db.Column(db.String(200), nullable=False)
    rank = db.Column(db.PickleType, default=[])
    def __repr__(self):
        return '<Query %r>' % self.id

@ranker2.route('/', methods=['POST', 'GET'])
def index():
    query = Ranking.query.one_or_none()
    if request.method == 'POST':
        print("pos")
        global ranks
        if ranks == []:
            ranks = rankerer.GameRank()
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
        #curGame = Gamers.query.get_or_404(200000)
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
        return render_template('index.html', ranks=[])

if __name__ == "__main__":
    ranker2.run(debug=True)