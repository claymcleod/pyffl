import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nflgame
import argparse
from datetime import date
from collections import defaultdict
from transformers import *
from utility import DynamicClassLoader

parser = argparse.ArgumentParser(description='Update player data')
parser.add_argument('transformer', metavar='T', type=str,
                    help='Transformer to execute')
parser.add_argument("-y", "--years", default=[2015], type=int, nargs='+',
                    help="The years to process")

args = parser.parse_args()
games_to_search = defaultdict(set)
transformer = globals()[args.transformer]()
today = date.today()

transformer.setup()

for scheduled_game in nflgame.sched.games.values():
    if scheduled_game["year"] not in args.years or scheduled_game["season_type"] != "REG":
        continue
    game_date = date(scheduled_game["year"], scheduled_game[
                     "month"], scheduled_game["day"])
    if game_date > today:
        break
    games_to_search[scheduled_game["year"]].add(scheduled_game["week"])

for year in games_to_search:
    for week in games_to_search[year]:
        games = nflgame.games(year, week=week)
        for game in games:
            transformer.parse_game(game, year, week)

transformer.finish()
