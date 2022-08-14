import nltk
nltk.data.path.append('./nltk_data/')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re

class tokeners:
    def __init__(self, extra=['zero','one','two','three','four','five','six','seven',
                   'eight','nine','ten','may','also','across','among','beside',
                   'however','yet','within', 'game', 'player']): #"games", "game", "gaming", "gamer", "play", "playing"
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.update(extra)
        self.stemmer = SnowballStemmer("english")
        self.re_stop_words = re.compile(r"\b(" + "|".join(self.stop_words) + ")\\W", re.I)

    def tokenize(self, text):
        words = re.findall(r'\w+', text)
        words = [self.stemmer.stem(x.lower()) for x in self.re_stop_words.sub("", " ".join(words)).split(" ")]
        return words

    def tokening(self, text):
        words = re.findall(r'\w+', text)
        words = " ".join([self.stemmer.stem(x.lower()) for x in words])
        return words

    def bagOWords(self, curDict):
        bow = []
        if "summary" in curDict:
            bow.append(curDict["summary"])
        if "name" in curDict:
            bow.append(curDict["name"])
        if "game_modes" in curDict:
            for mode in curDict["game_modes"]:
                bow.append(mode["name"])
        if "genres" in curDict:
            for genre in curDict["genres"]:
                bow.append(genre["name"])
        if "themes" in curDict:
            for theme in curDict["themes"]:
                bow.append(theme["name"])
        if "platforms" in curDict:
            for platform in curDict["platforms"]:
                bow.append(platform["name"])
        if "player_perspectives" in curDict:
            for pp in curDict["player_perspectives"]:
                bow.append(pp["name"])
        return self.tokenize(" ".join(bow))

    def bagODetails(self, curDict):
        bow = []
        if "summary" in curDict:
            bow = self.tokenize(curDict["summary"])
        if "name" in curDict:
            bow += self.tokenize(curDict["name"])
        if "game_modes" in curDict:
            for mode in curDict["game_modes"]:
                bow.append(mode["name"])
        if "genres" in curDict:
            for genre in curDict["genres"]:
                bow.append(genre["name"])
        if "themes" in curDict:
            for theme in curDict["themes"]:
                bow.append(theme["name"])
        if "platforms" in curDict:
            for platform in curDict["platforms"]:
                bow.append(platform["name"])
        if "player_perspectives" in curDict:
            for pp in curDict["player_perspectives"]:
                bow.append(f"playerP{pp}")
        return bow