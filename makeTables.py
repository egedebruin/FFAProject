import pandas as pd

types = ['dmu', 'ta', 'la', 'swv', 'orb', 'abz', 'yn', 'ft', '']
results = {
            'Instance type': [],
            'Number of instances': [],
            'HC-Average': [],
            'FFA-Average': [],
            'HC-Better': [],
            'FFA-Better': [],
            'HC-BKS': [],
            'FFA-BKS': [],
        }
comparisonResults = {
    'Instance type': [],
    'Number of instances': [],
    'HC-Best': [],
    'HC-Mean': [],
    'FFA-Best': [],
    'FFA-Mean': [],
    'HC-Best Weise': [],
    'HC-Mean Weise': [],
    'FFA-Best Weise': [],
    'FFA-Mean Weise': [],
}

df = pd.read_csv('files/output/hc2/allResults.csv')
weiseDf = pd.read_csv('files/weiseResults.csv')
bestDf = df.groupby('instance').min().reset_index()
averageDf = df.groupby('instance').mean().reset_index()

for instanceType in types:
    typeDf = df[df['instance'].str.match(instanceType)]
    if instanceType == '':
        results['Instance type'].append('All')
    else:
        results['Instance type'].append(instanceType)
    results['Number of instances'].append(int(len(typeDf) / 5))
    results['HC-Average'].append(round(typeDf['hc'].mean(), 1))
    results['FFA-Average'].append(round(typeDf['ffa'].mean(), 1))
    results['HC-Better'].append(sum(typeDf['hc'] < typeDf['ffa']) / 5)
    results['FFA-Better'].append(sum(typeDf['ffa'] < typeDf['hc']) / 5)
    results['HC-BKS'].append(sum(typeDf['hc'] == typeDf['bks']) / 5)
    results['FFA-BKS'].append(sum(typeDf['ffa'] == typeDf['bks']) / 5)

    typeBestDf = bestDf[bestDf['instance'].str.match(instanceType)]
    typeMeanDf = averageDf[averageDf['instance'].str.match(instanceType)]
    typeWeiseDf = weiseDf[weiseDf['instance'].str.match(instanceType)]
    if instanceType == '':
        comparisonResults['Instance type'].append('All')
    else:
        comparisonResults['Instance type'].append(instanceType)
    comparisonResults['Number of instances'].append(int(len(typeDf) / 5))
    comparisonResults['HC-Best'].append(round(typeBestDf['hc'].mean(), 1))
    comparisonResults['HC-Mean'].append(round(typeMeanDf['hc'].mean(), 1))
    comparisonResults['FFA-Best'].append(round(typeBestDf['ffa'].mean(), 1))
    comparisonResults['FFA-Mean'].append(round(typeMeanDf['ffa'].mean(), 1))
    comparisonResults['HC-Best Weise'].append(round(typeWeiseDf['hcBest'].mean(), 1))
    comparisonResults['HC-Mean Weise'].append(round(typeWeiseDf['hcMean'].mean(), 1))
    comparisonResults['FFA-Best Weise'].append(round(typeWeiseDf['ffaBest'].mean(), 1))
    comparisonResults['FFA-Mean Weise'].append(round(typeWeiseDf['ffaMean'].mean(), 1))

resultDf = pd.DataFrame(results)
comparisonDf = pd.DataFrame(comparisonResults)

resultDf.to_csv('own_results.csv', index=False)
comparisonDf.to_csv('comparison_results.csv', index=False)
