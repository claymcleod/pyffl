import pandas
df = pandas.read_csv('./data/players.csv')

# example showing most passing yds from the current dataset
print df.sort(['passing_yds'], ascending=[0]).head(5)[["name", "week", "year", "home", "away", "passing_yds"]]