import json
import pickle

games = pickle.load(open("data/index.pkl", 'rb'))
gameList = pickle.load(open("data/indexList.pkl", 'rb'))
wordBank = pickle.load(open("data/wordBank.pkl", 'rb'))

json.dump(games, open("games.json", 'w'))
json.dump(gameList, open("gameList.json", 'w'))
json.dump(wordBank, open("wordBank.json", 'w'))