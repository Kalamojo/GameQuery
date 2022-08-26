# RAPI

RAPI, short for Ranking API, is a querying application with access to IGDB's game database. Given a search, it returns the 20 (or less) most relevant games available.

In addition to general searches, RAPI supports boolean operations:

| Type of Query | Example | Effect |
|---------------|---------|--------|
| Or | pokemon or dragon ball | Returns the most relevant games from either part of the query |
| And | horse and race | Returns only the games that contain words from both parts of the query |
| String Literal | "super smash bros" | Returns only the games that have the query wrapped in quotes in-order |

Searches are made by adding "/api/rank?query=" to the url, along with a search.

### Example

Url: https://gamequery.herokuapp.com/api/rank?query=dragon+ball+and+z

First Game: {"id":78235,"name":"Dragon Ball Z: Dragon Battlers","summary":"Data Carddass Dragon Ball Kai Dragon Battlers was released in 2009 only in Japan, in arcade. It was the first game to have Super Saiyan 3 Broly as well as Super Saiyan 3 Vegeta. This game is based off of characters from Dragon Ball Z. The game's main feature is having two characters use a team attack such as Gotenks and Gogeta or Cell and Frieza. The graphics are similar to Dragon Ball Z: Budokai 3 and Dragon Ball Z: Infinite World.","url":"https://www.igdb.com/games/dragon-ball-z-dragon-battlers", "words":["data","carddass","dragon","ball","kai","dragon","battler","releas","2009","japan","arcad","first","super","saiyan","3","broli","well","super","saiyan","3","vegeta","base","charact","dragon","ball","z","main","featur","charact","use","team","attack","gotenk","gogeta","cell","frieza","graphic","similar","dragon","ball","z","budokai","3","dragon","ball","z","infinit","world","dragon","ball","z","dragon","battler"]}

## How it Works

~~~
