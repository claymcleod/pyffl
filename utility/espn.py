class ESPNUtility(object):

    @staticmethod
    def transform_standard_points(row):
        passing_tds = row['passing_tds'] if 'passing_tds' in row else 0
        passing_yds = row['passing_yds'] if 'passing_yds' in row else 0
        rushing_tds = row['rushing_tds'] if 'rushing_tds' in row else 0
        rushing_yds = row['rushing_yds'] if 'rushing_yds' in row else 0
        receiving_yds = row['receiving_yds'] if 'receiving_yds' in row else 0
        receiving_tds = row['receiving_tds'] if 'receiving_tds' in row else 0
        return passing_tds * 4 + (passing_yds // 25) + rushing_tds * 6 + rushing_yds // 10 + receiving_tds * 6 + receiving_yds // 10
