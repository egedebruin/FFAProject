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

weiseResults = {
            'Instance type': [],
            'Number of instances': [],
            'HC-Average': [],
            'FFA-Average': [],
            'HC-Better': [],
            'FFA-Better': [],
            'HC-BKS': [],
            'FFA-BKS': [],
        }

ownResults = {
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
weiseDf = pd.read_csv('files/results/weiseResultsOriginal.csv')
bestDf = df.groupby('instance').min().reset_index()
averageDf = df.groupby('instance').mean().reset_index()

for instanceType in types:
    typeDf = averageDf[averageDf['instance'].str.match(instanceType)].sort_values(by=['instance']).reset_index()
    typeWeiseDf = weiseDf[weiseDf['instance'].str.match(instanceType)].sort_values(by=['instance']).reset_index()

    hcAverage = round(typeDf['hc'].mean(), 1)
    ffaAverage = round(typeDf['ffa'].mean(), 1)
    hcBetter = sum(typeDf['hc'] < typeDf['ffa'])
    ffaBetter = sum(typeDf['ffa'] < typeDf['hc'])
    hcBks = sum(typeDf['hc'] == typeDf['bks'])
    ffaBks = sum(typeDf['ffa'] == typeDf['bks'])
    whcAverage = round(typeWeiseDf['hc'].mean(), 1)
    wffaAverage = round(typeWeiseDf['ffa'].mean(), 1)
    whcBetter = sum(typeWeiseDf['hc'] < typeWeiseDf['ffa'])
    wffaBetter = sum(typeWeiseDf['ffa'] < typeWeiseDf['hc'])
    whcBks = sum(typeWeiseDf['hc'] == typeDf['bks'])
    wffaBks = sum(typeWeiseDf['ffa'] == typeDf['bks'])

    if instanceType == '':
        weiseResults['Instance type'].append('All')
    else:
        weiseResults['Instance type'].append(instanceType)
    weiseResults['Number of instances'].append(int(len(typeDf)))
    weiseResults['HC-Average'].append(whcAverage)
    weiseResults['FFA-Average'].append(wffaAverage)
    weiseResults['HC-Better'].append(whcBetter)
    weiseResults['FFA-Better'].append(wffaBetter)
    weiseResults['HC-BKS'].append(whcBks)
    weiseResults['FFA-BKS'].append(wffaBks)

    if instanceType == '':
        ownResults['Instance type'].append('All')
    else:
        ownResults['Instance type'].append(instanceType)
    ownResults['Number of instances'].append(int(len(typeDf)))
    ownResults['HC-Average'].append(hcAverage)
    ownResults['FFA-Average'].append(ffaAverage)
    ownResults['HC-Better'].append(hcBetter)
    ownResults['FFA-Better'].append(ffaBetter)
    ownResults['HC-BKS'].append(hcBks)
    ownResults['FFA-BKS'].append(ffaBks)

    if instanceType == '':
        results['Instance type'].append('All')
    else:
        results['Instance type'].append(instanceType)
    results['Number of instances'].append(int(len(typeDf)))
    results['HC-Average'].append(str(round(((hcAverage * 100) / whcAverage) - 100, 3)) + '%')
    results['FFA-Average'].append(str(round(((ffaAverage * 100) / wffaAverage) - 100, 3)) + '%')
    if whcBetter == 0:
        if hcBetter > 0:
            results['HC-Better'].append('100%')
        else:
            results['HC-Better'].append('0%')
    else:
        results['HC-Better'].append(str(round(((hcBetter * 100) / whcBetter) - 100, 3)) + '%')
    if wffaBetter == 0:
        if ffaBetter > 0:
            results['FFA-Better'].append('100%')
        else:
            results['FFA-Better'].append('0%')
    else:
        results['FFA-Better'].append(str(round(((ffaBetter * 100) / wffaBetter) - 100, 3)) + '%')
    if whcBks == 0:
        if hcBks > 0:
            results['HC-BKS'].append('100%')
        else:
            results['HC-BKS'].append('0%')
    else:
        results['HC-BKS'].append(str(round(((hcBks * 100) / whcBks) - 100, 3)) + '%')
    if wffaBks == 0:
        if ffaBks > 0:
            results['FFA-BKS'].append('100%')
        else:
            results['FFA-BKS'].append('0%')
    else:
        results['FFA-BKS'].append(str(round(((ffaBks * 100) / wffaBks) - 100, 3)) + '%')

resultDf = pd.DataFrame(results)
comparisonDf = pd.DataFrame(comparisonResults)
weiseDf2 = pd.DataFrame(weiseResults)
ownDf = pd.DataFrame(ownResults)

weiseDf2.to_csv('weise_results.csv', index=False)
resultDf.to_csv('comparison_results.csv', index=False)
ownDf.to_csv('own_results.csv', index=False)
