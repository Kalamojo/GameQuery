from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json

indexer2 = Flask(__name__)
indexer2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gameRepo.db'
indexer2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(indexer2)

class Repos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gameList = db.Column(db.String, nullable=False)
    wordBank = db.Column(db.PickleType, nullable=False)
    def __repr__(self):
        return '<Repo %r>' % self.id

@indexer2.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        gameList = json.load(open("indexList.json"))
        wordBank = json.load(open("wordBank.json"))
        for i in range(len(gameList)):
            c = str(i)
            newRepo = Repos(gameList=gameList[i], wordBank=wordBank[c])
            db.session.add(newRepo)
        
        db.session.commit()
        return "Nice, it worked"
    else:
        return render_template('index.html', ranks=[])

if __name__ == "__main__":
    indexer2.run(debug=True)