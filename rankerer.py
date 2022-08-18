from ntlkTools import tokeners
from collections import defaultdict
from heapq import nlargest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import shlex
import ranker2
#from sklearn.metrics import jaccard_score


class GameRank:
    def __init__(self):
        self.tokener = tokeners()
        self.gameList = []
        for rep in ranker2.Repos.query.all():
            self.gameList.append(rep.gameList)
        self.count = TfidfVectorizer() #use_idf=True,smooth_idf=True,sublinear_tf=False,analyzer='word',max_df=0.5, min_df=0.0005,max_features=None
        self.count_matrix = self.count.fit_transform(self.gameList)
        #self.cosine_sim_matrix = cosine_similarity(self.count_matrix, self.count_matrix)

    def idToInd(self, gid):
        gid = int(gid)
        for ind in range(len(self.gameList)):
            #print(self.games[ind]['id'])
            game = ranker2.Gamers.query.get_or_404(ind+1)
            if game.ind == gid:
                return ind
        print("Game not found")
        return 0

    def rankG(self, query, matrix, index, vec, top=20):
        ids = []
        ranking = {}
        query = self.tokener.tokenize(query)
        cosine_sim = cosine_similarity(matrix, vec.transform(query))
        d = defaultdict(list)
        for i in range(len(cosine_sim)):
            for j in range(len(query)):
                d[cosine_sim[i][j]].append((i, j))
        for value, positions in nlargest(top, d.items(), key=lambda item: item[0]):
            if index[str(positions[0][0])].ind not in ids:
                ranking[value] = index[str(positions[0][0])]
                ids.append(index[str(positions[0][0])].ind)
        return ranking

    def rank1(self, query, top=20):
        ids = []
        ranking = {}
        query = self.tokener.tokenize(query)
        cosine_sim = cosine_similarity(self.count_matrix, self.count.transform(query))
        d = defaultdict(list)
        for i in range(len(cosine_sim)):
            for j in range(len(query)):
                d[cosine_sim[i][j]].append((i, j))
        for value, positions in nlargest(top, d.items(), key=lambda item: item[0]):
            game = ranker2.Gamers.query.get_or_404(positions[0][0]+1)
            if game.ind not in ids:
                ranking[value] = game
                ids.append(game.ind) #getattr(game, "ind")
        return ranking

    def rank2(self, gid, top=10):
        ids = [gid]
        ranking = {}
        idx = self.idToInd(gid)
        query = self.gameList[idx].split(" ")
        cosine_sim = cosine_similarity(self.count_matrix, self.count.transform(query))
        d = defaultdict(list)
        for i in range(len(cosine_sim)):
            for j in range(len(query)):
                d[cosine_sim[i][j]].append((i, j))
        for value, positions in nlargest(top, d.items(), key=lambda item: item[0]):
            game = ranker2.Gamers.query.get_or_404(positions[0][0]+1)
            if game.ind not in ids:
                ranking[value] = game
                ids.append(game.ind)
        return ranking

    def rank2b(self, gid, top=10):
        ids = []
        ranking = {}
        first = True
        idx = [ind for ind in range(len(self.gameList)) if ranker2.Gamers.query.get_or_404(ind+1).ind == gid][0]
        d = defaultdict(list)
        for j in range(len(self.cosine_sim_matrix[idx])):
            d[self.cosine_similarity_matrix[idx][j]].append((idx, j))
        c = 1
        for value, positions in nlargest(top+1, d.items(), key=lambda item: item[0]):
            if first:
                first = False
                continue;
            game = ranker2.Gamers.query.get_or_404(positions[0][0]+1)
            if game.ind not in ids:
                ranking[value] = game
                ids.append(game.ind)
        return ranking

    def print_rank(self, ranking, top=5):
        if len(ranking) == 0:
            print("No Search Results")
        else:
            times = 0
            for value, positions in nlargest(top, ranking.items(), key=lambda item: item[0]):
                if value != 0:
                    print(value, positions.name)
                    print("id:", positions.ind)
                    if "summary" in positions:
                        print(positions.summary)
                    print('')
                    times += 1
                else:
                    if times == 0:
                        print("No Search Results")
                    break;

    def get_rank(self, ranking, top=20):
        rank = []
        if len(ranking) != 0:
            times = 0
            for value, positions in nlargest(top, ranking.items(), key=lambda item: item[0]):
                if value != 0:
                    rank.append(positions)
                    times += 1
                else:
                    if times == 0:
                        break;
        return rank

    def query_bool(self, query):
        query_s = query.split(" ")
        if "and" in query_s or "or" in query_s or query.count('"') >= 2 or 'not' in query_s:
            return True
        return False

    def bool_queries(self, query_s, cond):
        lists = []
        lists.append([])
        c = 0
        for i in range(len(query_s)):
            if query_s[i] == cond:
                c += 1
                lists.append([])
            elif query_s[i] == 'not':
                continue;
            elif query_s[i-1] == 'not':
                lists[c].append('not ' + query_s[i])
            else:
                lists[c].append(query_s[i])
        return lists

    def and_dicts(self, queries):
        def inv_make(query):
            ind = defaultdict(dict)
            #c = 0
            for i in range(len(self.gameList)):
                rep = ranker2.Repos.query.get_or_404(i+1)
                game = ranker2.Gamers.query.get_or_404(i+1)
                i = str(i)
                adds = True
                for q in query:
                    if q in rep.wordBank:
                        adds = False
                        break;
                if adds:
                    ind[i]['ind'] = game.ind
                    #setattr(ind[i], 'ind', game.ind)
                    ind[i]['name'] = game.name
                    #setattr(ind[i], 'name', game.name)
                    ind[i]['url'] = game.url
                    #setattr(ind[i], 'url', game.url)
                    if game.summary:
                        ind[i]['summary'] = game.summary
                    ind[i]['words'] = rep.wordBank
            return ind
        def ind_make(query):
            ind = defaultdict(dict)
            #c = 0
            for i in range(len(self.gameList)):
                rep = ranker2.Repos.query.get_or_404(i+1)
                game = ranker2.Gamers.query.get_or_404(i+1)
                i = str(i)
                adds = True
                for q in query:
                    if q not in rep.wordBank:
                        adds = False
                        break;
                if adds:
                    ind[i]['ind'] = game.ind
                    #setattr(ind[i], 'ind', game.ind)
                    ind[i]['name'] = game.name
                    #setattr(ind[i], 'name', game.name)
                    ind[i]['url'] = game.url
                    #setattr(ind[i], 'url', game.url)
                    if game.summary:
                        ind[i]['summary'] = game.summary
                    ind[i]['words'] = rep.wordBank
            return ind

        dicts = []
        for query in queries:
            if query[0][:4] == 'not ':
                #print("nope", query[0])
                dicts.append(inv_make(self.tokener.tokenize(query[0])))
                #print(differ(index, ind_make(self.tokener.tokenize(query[0]))))
            elif len(self.tokener.tokenize(query[0])) > 1:
                dicts.append(self.literals(self.tokener.tokenize(query[0])))
            else:
                dicts.append(ind_make(query))
        return dicts

    def literals(self, queries):
        def check2( l,i,j ): return i in l and j in l and l[-1] != i and l[l.index(i)+1] == j
        def check_more(l, vals): return any(vals == l[i:i+len(vals)] for i in range(len(l)))
        ind = {}
        #c = 0
        if len(queries) == 0:
            return ranker2.Gamers.query.all()
        elif len(queries) == 1:
            for i in range(len(self.gameList)):
                rep = ranker2.Repos.query.get_or_404(i+1)
                game = ranker2.Gamers.query.get_or_404(i+1)
                i = str(i)
                adds = True
                for q in queries[0]:
                    if q not in rep.wordBank:
                        adds = False
                        break;
                if adds:
                    ind[i] = game
                    ind[i]['words'] = getattr(rep, "wordBank")
        elif len(queries) == 2:
            for i in range(len(self.gameList)):
                rep = ranker2.Repos.query.get_or_404(i+1)
                game = ranker2.Gamers.query.get_or_404(i+1)
                i = str(i)
                if check2(rep.wordBank, queries[0], queries[1]):
                    ind[i] = game
                    ind[i]['words'] = getattr(rep, "wordBank")
                    #c += 1
        else:
            for i in range(len(self.gameList)):
                rep = ranker2.Repos.query.get_or_404(i+1)
                game = ranker2.Gamers.query.get_or_404(i+1)
                i = str(i)
                if check_more(rep.wordBank, queries):
                    ind[i] = game
                    ind[i]['words'] = getattr(rep, "wordBank")
                    #c += 1
        return ind

    def and_op(self, dicts, query):
        def Intersection(dicts):
            def Inter(d1, d2):
                d3 = {}
                shared_keys = d1.keys() & d2.keys()
                d3 = {k: d1[k] for k in shared_keys}
                """
                count = 0
                for val1 in d1.values():
                    for val2 in d2.values():
                        if val1[idt] == val2[idt]: #and val1[idt] not in [val[idt] for val in d3.values()]:
                            goes = True
                            for val in d3.values():
                                if val1[idt] == val[idt]:
                                    goes = False
                                    break;
                            if goes:
                                d3[count] = val1
                                count += 1
                """
                return d3
            comb = dicts[0]
            if len(dicts) == 1:
                pass;
            else:
                for i in range(1, len(dicts)):
                    comb = Inter(comb, dicts[i])
            newComb = {}
            c = 0
            for val in comb.values():
                newComb[str(c)] = val
                c += 1
            return newComb
        count_new = TfidfVectorizer()
        ranking = {}
        ind_list_new = []
        comb = Intersection(dicts)
        if len(comb) == 0:
            return ranking
        else:
            for val in comb.values():
                ind_list_new.append(" ".join(val['words']))
            count_matrix2 = count_new.fit_transform(ind_list_new)
            ranking = self.rankG(query, count_matrix2, comb, count_new)
        return ranking;

    def or_op(self, rankings):
        """
        def Merge(ds):
            d3 = {}
            for d in ds: # you can list as many input dicts as you want here
                for value, idx in d.items():
                    if idx not in d3.values():
                        d3[value] = idx
            return(d3)
        return Merge((rank for rank in rankings))
        """
        z = {}
        first = True
        for rank in rankings:
            if first:
                z = rank.copy()
                first = False
            else:
                z.update(rank)
        return z

    def negation(self, items):
        for item in items:
            if item[:4] == 'not ':
                return True
        return False

    def querier(self, query):
        query_s = [self.tokener.tokening(x) for x in shlex.split(query)]
        rankings = []
        lists = self.bool_queries(query_s, 'or')
        for item in lists:
            if 'and' in query_s or self.negation(item):
                query_n = self.bool_queries(item, 'and')
                if len(query_n) <= 1:
                    continue;
                dicts = self.and_dicts(query_n)
                ranking = self.and_op(dicts, " ".join(item))
            elif len(self.tokener.tokenize(item[0])) > 1:
                dict = self.literals(self.tokener.tokenize(item[0]))
                ranking = self.and_op([dict], " ".join(item))
            else:
                ranking = self.rank1(" ".join(item))
            rankings.append(ranking)
        return self.or_op(rankings)