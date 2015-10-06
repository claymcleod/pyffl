from transformer import Transformer
import pandas as pd

rows = []
class StandardPlayerTransformer(Transformer):

    @staticmethod
    def setup():
        pass

    @staticmethod
    def parse_game(game, year, week):

        for player in game.players:
            p = player.__dict__
            d = {
                "home": game.home,
                "away": game.away,
                "week": week,
                "year": year,
                "name": p["name"],
                "team": p["team"],
                "opponent": game.away if p["team"] == game.home else game.home
            }

            for k, v in player._stats.iteritems():
                d[k] = v

            rows.append(d)

    @classmethod
    def finish(cls):
        df = pd.DataFrame.from_dict(rows)
        df.index.name = "index"
        df.to_csv(Transformer.get_csv_filename(cls.__name__))
        df.to_pickle(Transformer.get_pickle_filename(cls.__name__))
