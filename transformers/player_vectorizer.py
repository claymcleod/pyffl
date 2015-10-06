from transformer import Transformer
import pandas as pd
import numpy as np
import gzip
import os
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction import DictVectorizer
import cPickle

rows = []
all_players = []
all_games = []
dv = DictVectorizer()

features = []
labels_home = []
labels_away = []
last_known_players = {}
futures_home = []
futures_away = []
future_games = []

class PlayerVectorizerTransformer(Transformer):

    @staticmethod
    def setup():
        pass

    @staticmethod
    def parse_game(game, year, week):
        home_players = []
        away_players = []
        for player in game.players:
            p = player.__dict__
            all_players.append({'name': p["name"]})
            if p["team"] == game.home:
                home_players.append({'name': p["name"]})
            else:
                away_players.append({'name': p["name"]})

        last_known_players[game.home] = home_players
        last_known_players[game.away] = away_players
        all_games.append((game, year, week))


    @staticmethod
    def parse_future_game(home, away, week, year):
        if week == 5:
            future_games.append((home, away, week, year))

    @classmethod
    def finish(cls):
        dv.fit(all_players)
        for (g, y, w) in all_games:
            this_games_players = list()
            for p in g.players:
                this_games_players.append({'name': p.__dict__["name"]})
            rows = dv.transform(this_games_players)
            result_array = None
            for row in rows:

                if result_array == None:
                    result_array = row
                else:
                    result_array = result_array + row

            features.append(result_array.toarray()[0])
            labels_home.append(g.score_home)
            labels_away.append(g.score_away)

        for (home, away, week, year) in future_games:
            rows = dv.transform(last_known_players[home] + last_known_players[away])
            result_array = None
            for row in rows:

                if result_array == None:
                    result_array = row
                else:
                    result_array = result_array + row

            futures_home.append({
                'name': home,
                'features': result_array.toarray()[0]
            })

            futures_away.append({
                'name': away,
                'features': result_array.toarray()[0]
            })

        train_home = (np.array(features), np.array(labels_home,))
        train_away = (np.array(features), np.array(labels_away,))

        dir_name = os.path.dirname(Transformer.get_pickle_filename(cls.__name__))
        train_home_name = os.path.join(dir_name, "train_home.pickle.gz")
        train_away_name = os.path.join(dir_name, "train_away.pickle.gz")
        future_home_name = os.path.join(dir_name, "futures_home.pickle.gz")
        future_away_name = os.path.join(dir_name, "futures_away.pickle.gz")
        cPickle.dump(train_home, gzip.open(train_home_name,'wb'), cPickle.HIGHEST_PROTOCOL)
        cPickle.dump(train_away, gzip.open(train_away_name,'wb'), cPickle.HIGHEST_PROTOCOL)
        cPickle.dump(futures_home, gzip.open(future_home_name,'wb'), cPickle.HIGHEST_PROTOCOL)
        cPickle.dump(futures_away, gzip.open(future_away_name,'wb'), cPickle.HIGHEST_PROTOCOL)
