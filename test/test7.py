from indexer import GameIndex
from ranker import GameRank
import pickle

print("starting")
#index = GameIndex()

#games = index.games
#gameList = index.gameList
#wordBank = index.wordBank

#ranks = GameRank(games, gameList, wordBank)
with open("data/ranks.pkl", 'rb') as fp:
    ranks = pickle.load(fp)
#monkey and space
print("New Search")
while(True):
    searchKey = input("\nEnter a query: ")
    if searchKey == '':
        break;
    elif ranks.query_bool(searchKey):
        ranks.print_rank(ranks.querier(searchKey))
    else:
        ranks.print_rank(ranks.rank1(searchKey))
