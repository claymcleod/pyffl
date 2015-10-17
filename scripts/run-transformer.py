import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import nflgame
import argparse
from datetime import date, timedelta
from collections import defaultdict
from transformers import *

parser = argparse.ArgumentParser(description='Update player data')
parser.add_argument('transformer', metavar='T', type=str,
                    help='Transformer to execute')
parser.add_argument("-y", "--years", default=[2015], type=int, nargs='+',
                    help="The years to process")

args = parser.parse_args()
games_to_search = defaultdict(set)
future_games = []
transformer = globals()[args.transformer]()
today = date.today() - timedelta(7)

transformer.setup()
future = False

for scheduled_game in nflgame.sched.games.values():
    if scheduled_game["year"] not in args.years or scheduled_game["season_type"] != "REG":
        continue
    game_date = date(scheduled_game["year"], scheduled_game[
                     "month"], scheduled_game["day"])
    if future or game_date > today:
        future = True
    if not future:
        games_to_search[scheduled_game["year"]].add(scheduled_game["week"])
    else:
        future_games.append({
            'home': scheduled_game["home"],
            'away': scheduled_game["away"],
            'week': scheduled_game["week"],
            'year': scheduled_game["year"],
        })

for year in games_to_search:
    for week in games_to_search[year]:
        games = nflgame.games(year, week=week)
        for game in games:
            transformer.parse_game(game, year, week)

if transformer.parse_future_game != None:
    for game in future_games:
        transformer.parse_future_game(game["home"], game["away"], game["week"], game["year"])

transformer.finish()
