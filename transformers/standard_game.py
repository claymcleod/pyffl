import urllib2
from bs4 import BeautifulSoup
import os.path
import pandas as pd
from utility.nflweather import NFLWeather

from transformer import Transformer
rows = []
weather_map = {}

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
            "year": year,
            "home_score": game.score_home,
            "away_score": game.score_away
        }

        _url = 'http://www.nflweather.com/week/%i/week-%i/' % (year, week)
        if not _url in weather_map:
            weather_map[_url] = True
            html = urllib2.urlopen(_url).read()
            soup = BeautifulSoup( html , "lxml")
            for a in soup.findAll('a', {'class': 'btn btn-success move-rigth'}):
                page_url = 'http://www.nflweather.com%s' % a["href"]
                page_html = urllib2.urlopen(page_url).read()
                page_soup = BeautifulSoup(page_html, "lxml")
                home_team = page_soup.find('div', {'class': 'g-home'}).find('a')['href']
                home_abbr = "%s-%i-%i" % (NFLWeather.link_to_name(home_team), year, week)
                the_dict = {}
                for div in page_soup.findAll('div', {'class': 'span5'}):
                    for p in div.findAll('p'):
                        t = p.text
                        if ':' in t:
                            key, value = map(lambda x: x.strip(), t.split(':'))
                            the_dict[key] = StandardGameTransformer.parse_key_value(key, value)

                weather_map[home_abbr] = the_dict

        #f = urllib.urlopen()
        #print f

        for key, value in game.stats_home._asdict().iteritems():
            d["home_"+key] = StandardGameTransformer.parse_key_value(key, value)

        for key, value in game.stats_away._asdict().iteritems():
            d["away_"+key] = StandardGameTransformer.parse_key_value(key, value)

        current_abbr = "%s-%i-%i" % (game.home, year, week)
        if current_abbr in weather_map:
            for k, v in weather_map[current_abbr].iteritems():
                d[k] = v

        rows.append(d)

    @staticmethod
    def parse_key_value(key, value):
        if key == 'Barometer':
            return int(value.replace("\"",""))
        elif key == 'Cloud Cover' or key == 'Humidity' or key == 'Precipitation Prob.':
            return int(value.replace("%", ""))
        elif key == 'Dew Point' or key == 'Feels like' or key == 'Temperature':
            if '/' in value:
                value = value.split('/')[0]
            return int(value.replace("f.",""))
        elif key == 'Visibility':
            return int(value.replace("mi", ""))
        elif key == 'pos_time':
            values = str(value).split(":")
            return int(values[1]) + 60*int(values[0])
        return value

    @classmethod
    def finish(cls):
        df = pd.DataFrame.from_dict(rows)
        df.index.name = "index"
        df.to_csv(Transformer.get_csv_filename(cls.__name__))
        df.to_pickle(Transformer.get_pickle_filename(cls.__name__))
