from hook import *
from sklearn.feature_extraction import DictVectorizer
dv = DictVectorizer()
all_players = []
class StandardCombinedHook(Hook):

    @classmethod
    def dependencies(cls):
        return ["StandardGameTransformer", "StandardPlayerTransformer"]

    @classmethod
    def run(cls):
        for player in dfs["StandardPlayerTransformer"].T.to_dict().values():
            all_players.append({'name': player["name"], 'year': player['year']})
        dv.fit(all_players)
        for player in dfs["StandardPlayerTransformer"].T.to_dict().values():
            for game in dfs["StandardGameTransformer"].T.to_dict().values():
                if game["home"] == player["team"] or game["away"] == player["team"]:
                    if game["week"] == player["week"] and game["year"] == player["year"]:
                        print "Found!"
                        break
