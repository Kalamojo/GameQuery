from ntlkTools import tokeners
import requests
import json
import pickle
from pathlib import Path

class GameIndex:
    def __init__(self):
        self.tokener = tokeners()
        self.indexPath = "data/index.pkl"
        self.listPath = "data/indexList.pkl"
        self.wordPath = "data/wordBank.pkl"
        self.textPath = "data/textBank.pkl"
        self.ofs = 0
        self.max_offset = 200500
        self.offstep = 500
        self.games, self.gameList, self.wordBank, self.textBank = self.newIndex()
    
    def newIndex(self):
        games = {}
        gameList = []
        wordBank = []
        textBank = []
        indexFile = Path(self.indexPath)
        listFile = Path(self.listPath)
        wordFile = Path(self.wordPath)
        textFile = Path(self.textPath)
        if indexFile.is_file() and listFile.is_file() and wordFile.is_file() and textFile.is_file():
            with open(self.indexPath, 'rb') as f:
                    games = pickle.load(f)
            with open(self.listPath, 'rb') as f:
                    gameList = pickle.load(f)
            with open(self.wordPath, 'rb') as f:
                    wordBank = pickle.load(f)
            with open(self.textPath, 'rb') as f:
                    textBank = pickle.load(f)
            print('load index: ' + self.indexPath + ', load list: ' + self.listPath)
        else:
            print('new index', 'new list')
            while self.ofs <= self.max_offset:
                if self.ofs % 10000 == 0:
                    print(self.ofs)
                r = requests.post("https://api.igdb.com/v4/games", headers={"Client-ID":"iandccesnxkg8eos8outaqkdjmcxkl", "Authorization":"Bearer uzjcv1er26qvwwyawqsqwjx4ghio13"}, 
                                data=f"fields name, genres.name, themes.name, summary, url; limit {self.offstep}; offset {self.ofs};")
                #fields name, genres.name, themes.name, platforms.name, player_perspectives.name, game_modes.name, summary, url
                #jsonText = json.loads(r.text)
                #if len(jsonText) == 0:
                #    break;
                gameList += json.loads(r.text)
                self.ofs += self.offstep
            print(self.ofs)
            for c in range(len(gameList)):
                games[c] = gameList[c]
                gameList[c] = " ".join(self.tokener.bagOWords(games[c]))
                wordBank[c] = self.tokener.bagOWords(games[c])
            
            """
            with open(self.indexPath, 'wb') as f:
                pickle.dump(games, f)
            with open(self.listPath, 'wb') as f:
                pickle.dump(gameList, f)
            with open(self.wordPath, 'wb') as f:
                pickle.dump(wordBank, f)
            with open(self.textPath, 'wb') as f:
                pickle.dump(textBank, f)
            """
            json.dump(games, open("games.json", 'w'))
            json.dump(gameList, open("gameList.json", 'w'))
            json.dump(wordBank, open("wordBank.json", 'w'))
        return games, gameList, wordBank, textBank