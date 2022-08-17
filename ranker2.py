from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json

ranker2 = Flask(__name__)
ranker2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
ranker2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(ranker2)

ranks = []

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

@ranker2.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        curGame = Gamers.query.get_or_404(200000)
        return curGame.summary
    else:
        return render_template('index.html', ranks=[])

if __name__ == "__main__":
    ranker2.run(debug=True)