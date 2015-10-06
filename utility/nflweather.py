d = {
    '/team/Cardinals': 'ARI',
    '/team/Falcons': 'ATL',
    '/team/Ravens': 'BAL',
    '/team/Bills': 'BUF',
    '/team/Panthers': 'CAR',
    '/team/Bears': 'CHI',
    '/team/Bengals': 'CIN',
    '/team/Browns': 'CLE',
    '/team/Broncos': 'DEN',
    '/team/Cowboys': 'DAL',
    '/team/Colts': 'IND',
    '/team/Jaguars': 'JAC',
    '/team/Lions': 'DET',
    '/team/Packers': 'GB',
    '/team/Texans': 'HOU',
    '/team/Chiefs': 'KC',
    '/team/Dolphins': 'MIA',
    '/team/Patriots': 'NE',
    '/team/Vikings': 'MIN',
    '/team/Saints': 'NO',
    '/team/Giants': 'NYG',
    '/team/Jets': 'NYJ',
    '/team/Raiders': 'OAK',
    '/team/Eagles': 'PHI',
    '/team/Steelers': 'PIT',
    '/team/Chargers': 'SD',
    '/team/Seahawks': 'SEA',
    '/team/49ers': 'SF',
    '/team/Rams': 'STL',
    '/team/Buccaneers': 'TB',
    '/team/Titans': 'TEN',
    '/team/Redskins': 'WAS'
}

class NFLWeather(object):

    @staticmethod
    def link_to_name(href):
        if not href in d:
            return ""
        else: return d[href]
