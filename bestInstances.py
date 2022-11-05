import pandas as pd

df = pd.read_csv('files/output/hc2/allResults.csv')

averageDf = df.groupby('instance').mean().reset_index()

averageDf['ratio'] = (averageDf['hc'] / averageDf['ffa'])

print(averageDf.sort_values(by=['ratio']))