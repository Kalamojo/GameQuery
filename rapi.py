from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from ranker import GameRank

rapi = Flask(__name__)
rapi.config['SQLALCHEMY_BINDS'] = {
    'db1': 'sqlite:///ranking.db',
    'db2': 'sqlite:///ranks.db',
    'db3': 'sqlite:///index.db'
}