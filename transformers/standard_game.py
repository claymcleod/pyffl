import urllib2
from bs4 import BeautifulSoup
import os.path
import pandas as pd

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
            "year": year
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
                for div in page_soup.findAll('div', {'class': 'span5'}):
                    for p in div.findAll('p'):
                        t = p.text
                        if ':' in t:
                            key, value = t.split(':')
                            print key, value

        #f = urllib.urlopen()
        #print f

        for key, value in game.stats_home._asdict().iteritems():
            d["home_"+key] = value

        for key, value in game.stats_away._asdict().iteritems():
            d["away_"+key] = value

        rows.append(d)

    @classmethod
    def finish(cls):
        df = pd.DataFrame.from_dict(rows)
        df.index.name = "index"
        df.to_csv(Transformer.get_csv_filename(cls.__name__))
        df.to_pickle(Transformer.get_pickle_filename(cls.__name__))
