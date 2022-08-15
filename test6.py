import pickle

print("start")
games = pickle.load(open("data/index.pkl", 'rb'))
gameList = pickle.load(open("data/indexList.pkl", 'rb'))
print("end")