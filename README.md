# RAPI

RAPI, short for Ranking API, is a querying application with access to IGDB's game database. Given a search, it returns the 20 (or less) most relevant games available.

In addition to general searches, RAPI supports boolean operations:

| Type of Query | Example | Effect |
|---------------|---------|--------|
| Or | pokemon or dragon ball | Returns the most relevant games from either part of the query |
| And | horse and race | Returns only the games that contain words from both parts of the query |
| String Literal | "super smash bros" | Returns only the games that have the query wrapped in quotes in-order |

Searches are made by adding "/api/rank?query=" to the url, along with a search.

#### Example

> Url: https://gamequery.herokuapp.com/api/rank?query=dragon+ball+and+z
> 
> First Game: 
> ```json
> {"id":78235,"name":"Dragon Ball Z: Dragon Battlers","summary":"Data Carddass Dragon Ball Kai Dragon Battlers was released in 2009 only in Japan, in arcade. It was the first game to have Super Saiyan 3 Broly as well as Super Saiyan 3 Vegeta. This game is based off of characters from Dragon Ball Z. The game's main feature is having two characters use a team attack such as Gotenks and Gogeta or Cell and Frieza. The graphics are similar to Dragon Ball Z: Budokai 3 and Dragon Ball Z: Infinite World.","url":"https://www.igdb.com/games/dragon-ball-z-dragon-battlers","words":["data","carddass","dragon","ball","kai","dragon","battler","releas","2009","japan","arcad","first","super","saiyan","3","broli","well","super","saiyan","3","vegeta","base","charact","dragon","ball","z","main","featur","charact","use","team","attack","gotenk","gogeta","cell","frieza","graphic","similar","dragon","ball","z","budokai","3","dragon","ball","z","infinit","world","dragon","ball","z","dragon","battler"]}
> ```

## How it Works

1. A given query is broken down into a vector of token frequencies.
2. That query is scanned for boolean operations, and games are filtered based on any operations found.
3. The remaining games (also represented as vectors of token frequencies) are cross-analyzed with the query vector to find the cosine similarity between each game and the query.
4. The 20 most similar games are returned in their original form.

## How it Works (extended)

### Tokenization

First, before relevancy calculations can occur, each game description is broken down into tokens. Non-alphanumeric characters, spaces, and stopwords are filtered out using regular expressions and the NLTK library's store of stopwords. 
These stopwords are extremely common words that contribute little meaning to the text.

#### Example

> and, the, for, it, to, had, in, etc.

Next, after each word is reduced to lowercase form, each word is further reduced to their stem. Word stemming is a process which attempts to bring words to their root form. Words like "dogs" would change to "dog", and "running" to "run". This is performed to reduce redundancy in the model and to capture all connections between queries and game descriptions.

### Similarity

To effectively use the tokens of each game in calculations, game attributes need to be represented numerically. This is accomplished by calculating frequency of each token in every game. Thankfully, the scikit-learn library comes equipped with two modules that can achieve this automatically:

- CountVectorizer, and
- TfidfVectorizer

CountVectorizer simply finds the frequency of each token in each game and represents everything as a list of vectors. TfidfVectorizer (short for term frequency inverse-document frequency vectorizer) takes an extended approach. Instead of simply adding 1 to the count for each token encountered, it factors in the frequency of a given token in all documents.

#### Example

> The word "play" may occur 10 times in a given game description. However, while the frequency of the token is 10, the tfidf will be lower due to its high frequency in all game descriptions.
> 
> A description with the token "omniscient" will have a relatively high value for that space due to its uniqueness among all tokens from all descriptions.

With vectors of numbers (token counts) representing each game, cosine similarity can then be used to find how similar one game is to another (or how similar a query is to a game). Cosine similarity, quite simply, measures the angle between two lines. In data analysis, lines can be represented by vectors of numbers.

