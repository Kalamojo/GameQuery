from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json

indexer2 = Flask(__name__)
indexer2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
indexer2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(indexer2)

class Gamers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ind = db.Column(db.Integer, nullable=False)
    genres = db.Column(db.PickleType, nullable=True)
    themes = db.Column(db.PickleType, nullable=True)
    name = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=True)
    url = db.Column(db.String, nullable=False)
    def __repr__(self):
        return '<%r>' % self.name

@indexer2.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        games = json.load(open("index.json"))
        for i in range(len(games)):
            c = str(i)
            newGame = Gamers(ind=games[c]["id"], name=games[c]["name"], url=games[c]["url"])
            
            if "genres" in games[c]:
                newGame.genres = games[c]["genres"]
            if "themes" in games[c]:
                newGame.themes = games[c]["themes"]
            if "summary" in games[c]:
                newGame.summary = games[c]["summary"]
            
            db.session.add(newGame)
        
        db.session.commit()
        return "Nice, it worked"
    else:
        return render_template('index.html', ranks=[])

if __name__ == "__main__":
    indexer2.run(debug=True)