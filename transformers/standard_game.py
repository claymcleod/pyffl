import os.path
import pandas as pd

from transformer import Transformer
rows = []
csv_filename = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "csv", "games.csv")
pkl_filename = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "pickle", "games.pkl")

class StandardGameTransformer(Transformer):

    @staticmethod
    def setup():
        pass

    @staticmethod
    def parse_game(game, year, week):
        d = {
            "home": game.home,
            "away": game.away,
            "week": week,
            "year": year
        }

        for key, value in game.stats_home._asdict().iteritems():
            d["home_"+key] = value

        for key, value in game.stats_away._asdict().iteritems():
            d["away_"+key] = value

        rows.append(d)

    @staticmethod
    def finish():
        df = pd.DataFrame.from_dict(rows)
        df.index.name = "index"
        df.to_csv(csv_filename)
        df.to_pickle(pkl_filename)
