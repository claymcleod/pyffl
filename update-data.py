from datetime import date
import nflgame
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Update player data')
parser.add_argument("-y", "--years", default=[2015], type=int, nargs='+',
                    help="The years to process")

args = parser.parse_args()

today = date.today()
games_to_search = defaultdict(set)
allFields = set([])
entries = []

def parse_game(game, year, week):
	if game == None:
		return None

	for p in game.players:
		entry = {
			'week': week,
			'year': year,
			'home': game.home,
			'away': game.away,
			'name': p.name
		}

		for field, stat in p.stats.iteritems():
			allFields.add(field)
			entry[field] = stat

		entries.append(entry)

for scheduled_game in nflgame.sched.games.values():
	if scheduled_game["year"] not in args.years or scheduled_game["season_type"] != "REG":
		continue
	game_date = date(scheduled_game["year"], scheduled_game["month"], scheduled_game["day"])
	if game_date > today:
		break
	games_to_search[scheduled_game["year"]].add(scheduled_game["week"])

for year in games_to_search:
	for week in games_to_search[year]:
		games = nflgame.games(year, week=week)
		for game in games:
			parse_game(game, year, week)

for entry in entries:
	for field in allFields:
		if field not in entry:
			entry[field] = ""

import csv
keys = ["week", "year", "home", "away", "name"] + list(allFields)
with open('./data/players.csv', 'wb') as player_file:
    dict_writer = csv.DictWriter(player_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(entries)