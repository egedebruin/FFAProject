import json
import os
import sys
from collections import defaultdict

import pandas as pd
import matplotlib.pyplot as plt

from Experiments import Experiments
from Util import Util

# if __name__ == '__main__':
#     os.chdir(sys.argv[1])
#     library = Util.readFullLibrary('files/jssp-instances/full_full_library.txt')
#
#     Experiments.runPpaComparisonExperiment(library)

results = pd.read_csv('files/output/ppa/allResults.csv')
hcResults = pd.read_csv('files/output/hc/allResults.csv')

ppaBetter = 0
ffaSelectBetter = 0
ffaCompleteBetter = 0
ppaBest = 0
ffaSelectBest = 0
ffaCompleteBest = 0
ppaBks = 0
ffaSelectBks = 0
ffaCompleteBks = 0

amountHcBest = 0
amountPpaBest = 0
amountTies = 0

amount = 0
sumPpa = 0
sumFfaSelect = 0
sumFfaComplete = 0

ratioDict = {'instance': [],
             'ppa': [],
             'ffaSelect': [],
             'ffaComplete': []}
for index, value in results.iterrows():
    if value['ppa'] < value['ffaSelect'] and value['ppa'] < value['ffaComplete']:
        ppaBetter += 1
    if value['ffaSelect'] < value['ppa'] and value['ffaSelect'] < value['ffaComplete']:
        ffaSelectBetter += 1
    if value['ffaComplete'] < value['ppa'] and value['ffaComplete'] < value['ffaSelect']:
        ffaCompleteBetter += 1

    if value['ppa'] <= value['ffaSelect'] and value['ppa'] <= value['ffaComplete']:
        ppaBest += 1
    if value['ffaSelect'] <= value['ppa'] and value['ffaSelect'] <= value['ffaComplete']:
        ffaSelectBest += 1
    if value['ffaComplete'] <= value['ppa'] and value['ffaComplete'] <= value['ffaSelect']:
        ffaCompleteBest += 1

    if value['ppa'] == value['best known solution']:
        ppaBks += 1
    if value['ffaSelect'] == value['best known solution']:
        ffaSelectBks += 1
    if value['ffaComplete'] == value['best known solution']:
        ffaCompleteBks += 1

    hcRecord = hcResults.loc[hcResults['instance'] == value['instance']]
    bestHc = min(list(hcRecord['hc'])[0], list(hcRecord['hc'])[0])
    bestPpa = min(value['ppa'], value['ppa'])

    if bestHc < bestPpa:
        amountHcBest += 1
    elif bestPpa < bestHc:
        amountPpaBest += 1
    else:
        amountTies += 1

    ratioDict['instance'].append(value['instance'])
    ratioDict['ppa'].append(int(value['ppa']) / ((int(value['ffaSelect']) + int(value['ffaComplete'])) / 2))
    ratioDict['ffaSelect'].append(int(value['ffaSelect']) / ((int(value['ppa']) + int(value['ffaComplete'])) / 2))
    ratioDict['ffaComplete'].append(int(value['ffaComplete']) / ((int(value['ffaSelect']) + int(value['ppa'])) / 2))

    if 'ta' in value['instance']:
        amount += 1
        sumPpa += int(value['ppa'])
        sumFfaSelect += int(value['ffaSelect'])
        sumFfaComplete += int(value['ffaComplete'])


# print(amount)
# print(sumPpa/amount)
# print(sumFfaSelect/amount)
# print(sumFfaComplete/amount)

# df = pd.DataFrame.from_dict(ratioDict)
# df = df.sort_values('ppa')
# print(df)

# print(ppaBetter)
# print(ffaSelectBetter)
# print(ffaCompleteBetter)
# print()
# print(ppaBest)
# print(ffaSelectBest)
# print(ffaCompleteBest)
# print()
# print(ppaBks)
# print(ffaSelectBks)
# print(ffaCompleteBks)
# print()
# print(amountPpaBest)
# print(amountHcBest)
# print(amountTies)

# plt.scatter(range(1, 243), results['ppa'], s=20, marker='o', label='PPA')
# plt.scatter(range(1, 243), results['ffaSelect'], s=20, marker='^', label='PPA FFA Select')
# plt.scatter(range(1, 243), results['ffaComplete'], s=20, marker='s', label='PPA FFA Complete')
# plt.scatter(range(1, 243), hcResults['hc'], s=20, marker='P', label='HC')
# plt.scatter(range(1, 243), hcResults['ffa'], s=20, marker='p', label='HC FFA')
# plt.scatter(range(1, 243), results['best known solution'], s=20, marker='*', label='Best Known Solution')
# plt.xlabel('Instance')
# plt.ylabel('Objective Value')
# plt.legend()
# plt.show()

library = Util.readFullLibrary('files/jssp-instances/full_full_library.txt')
#Util.createFunctionEvaluationsPlotPpa('files/output/ppa/populations/1/', library, 'la38')
Util.plotBoth(library, ['swv05', 'dmu76'])


# from jssp.JSSPFactory import JSSPFactory
#
# library = Util.readFullLibrary('files/jssp-instances/full_full_library.txt')
#
# subFolders = ['ta77', 'ta76', 'dmu53', 'dmu75', 'dmu45', 'la38']
# resultFolder = 'files/output/ppa/populations/1/'
# yPPAs = []
# yFFAs = []
# yFFACompletes = []
# xPPAs = []
# xFFAs = []
# xFFACompletes = []
# titles = []
# for subFolder in subFolders:
#     jssp = JSSPFactory.generateJSSPFromFormat(library[subFolder])
#     fileName = resultFolder + subFolder + "/"
#     filePpa = open(fileName + 'ppaAllBest.txt')
#     fileFfaSelect = open(fileName + 'ffaSelectAllBest.txt')
#     fileFfaComplete = open(fileName + 'ffaCompleteAllBest.txt')
#
#     recordsPpa = filePpa.readline().split(', ')[:-1]
#     xPpa = []
#     yPpa = []
#     for record in recordsPpa:
#         xPpa.append(int(record.split(':')[0]))
#         yPpa.append(int(record.split(':')[1]))
#
#     recordsFfaSelect = fileFfaSelect.readline().split(', ')[:-1]
#     xFfaSelect = []
#     yFfaSelect = []
#     for record in recordsFfaSelect:
#         xFfaSelect.append(int(record.split(':')[0]))
#         yFfaSelect.append(int(record.split(':')[1]))
#
#     recordsFfaComplete = fileFfaComplete.readline().split(', ')[:-1]
#     xFfaComplete = []
#     yFfaComplete = []
#     for record in recordsFfaComplete:
#         xFfaComplete.append(int(record.split(':')[0]))
#         yFfaComplete.append(int(record.split(':')[1]))
#
#     yPPAs.append(yPpa)
#     yFFAs.append(yFfaSelect)
#     yFFACompletes.append(yFfaComplete)
#     xPPAs.append(xPpa)
#     xFFAs.append(xFfaSelect)
#     xFFACompletes.append(xFfaComplete)
#     titles.append(subFolder + "(" + str(jssp.amountMachines) + " machines and " + str(jssp.amountJobs) + " jobs)")
#
# fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex=True)
# ax1.plot(xPPAs[0], yPPAs[0], label='PPA Standard')
# ax1.plot(xFFAs[0], yFFAs[0], label='PPA FFA Select')
# ax1.plot(xFFACompletes[0], yFFACompletes[0], label='PPA FFA Complete')
# ax1.set_title(titles[0])
# ax2.plot(xPPAs[1], yPPAs[1])
# ax2.plot(xFFAs[1], yFFAs[1])
# ax2.plot(xFFACompletes[1], yFFACompletes[1])
# ax2.set_title(titles[1])
# ax3.plot(xPPAs[2], yPPAs[2])
# ax3.plot(xFFAs[2], yFFAs[2])
# ax3.plot(xFFACompletes[2], yFFACompletes[2])
# ax3.set_title(titles[2])
# ax4.plot(xPPAs[3], yPPAs[3])
# ax4.plot(xFFAs[3], yFFAs[3])
# ax4.plot(xFFACompletes[3], yFFACompletes[3])
# ax4.set_title(titles[3])
# ax5.plot(xPPAs[4], yPPAs[4])
# ax5.plot(xFFAs[4], yFFAs[4])
# ax5.plot(xFFACompletes[4], yFFACompletes[4])
# ax5.set_title(titles[4])
# ax6.plot(xPPAs[5], yPPAs[5])
# ax6.plot(xFFAs[5], yFFAs[5])
# ax6.plot(xFFACompletes[5], yFFACompletes[5])
# ax6.set_title(titles[5])
# plt.xscale('log')
# fig.text(0.5, 0.04, 'Function Evaluations', ha='center', fontsize=16)
# fig.text(0.04, 0.5, 'Objective Value (Execution time)', va='center', rotation='vertical', fontsize=16)
# handles, labels = ax1.get_legend_handles_labels()
# fig.legend(handles, labels, loc=9)
#
# plt.show()

# from jssp.JSSPFactory import JSSPFactory
# library = Util.readFullLibrary('files/jssp-instances/full_full_library.txt')
# resultFolder = 'files/output/ppa/populations/1/'
# instanceName = 'ta70'
#
# jssp = JSSPFactory.generateJSSPFromFormat(library[instanceName])
# fileName = resultFolder + instanceName + "/"
# filePpa = open(fileName + 'ppaAllPop.txt')
# fileFfaSelect = open(fileName + 'ffaSelectAllPop.txt')
# fileFfaComplete = open(fileName + 'ffaCompleteAllPop.txt')
#
# recordsPpa = filePpa.readline().split('; ')[:-1]
# xPpa = []
# yPpa = []
# for record in recordsPpa:
#     xPpa = xPpa + [int(record.split(':')[0])] * 40
#     yPpa = yPpa + list(map(int, record.split(':')[1].replace('[', '').replace(']', '').split(',')))
#
# recordsFfaSelect = fileFfaSelect.readline().split('; ')[:-1]
# xFfaSelect = []
# yFfaSelect = []
# for record in recordsFfaSelect:
#     xFfaSelect = xFfaSelect + [int(record.split(':')[0])] * 40
#     yFfaSelect = yFfaSelect + list(map(int, record.split(':')[1].replace('[', '').replace(']', '').split(',')))
#
# recordsFfaComplete = fileFfaComplete.readline().split('; ')[:-1]
# xFfaComplete = []
# yFfaComplete = []
# for record in recordsFfaComplete:
#     xFfaComplete = xFfaComplete + [int(record.split(':')[0])] * 40
#     yFfaComplete = yFfaComplete + list(map(int, record.split(':')[1].replace('[', '').replace(']', '').split(',')))
#
# plt.scatter(xPpa, yPpa, label='PPA', s=10)
# plt.scatter(xFfaSelect, yFfaSelect, label='FFA Select', s=10)
# plt.scatter(xFfaComplete, yFfaComplete, label='FFA Complete', s=10)
# plt.xscale('log')
# plt.legend()
# plt.xlabel('Function Evaluations')
# plt.ylabel('Objective Value')
# plt.title(instanceName + "(" + str(jssp.amountMachines) + " machines and " + str(jssp.amountJobs) + " jobs)")
# plt.show()

# resultFolder = 'files/output/ppa/populations/1/'
# instanceName = 'dmu76'
# fileName = resultFolder + instanceName + "/"
# fileFfa = open(fileName + 'ffaSelectCurrent.txt')
# fileFfa.readline()
# ffaArray1 = defaultdict(lambda: 0, json.loads(fileFfa.readline()))
# ffaArray1 = {int(k): int(v) for k, v in ffaArray1.items()}
# title1 = instanceName + "(" + str(20) + " machines and " + str(50) + " jobs)"
#
# instanceName = 'dmu76'
# fileName = resultFolder + instanceName + "/"
# fileFfa = open(fileName + 'ffaCompleteCurrent.txt')
# fileFfa.readline()
# ffaArray2 = defaultdict(lambda: 0, json.loads(fileFfa.readline()))
# ffaArray2 = {int(k): int(v) for k, v in ffaArray2.items()}
#
# instanceName = 'la35'
# fileName = resultFolder + instanceName + "/"
# fileFfa = open(fileName + 'ffaSelectCurrent.txt')
# fileFfa.readline()
# ffaArray3 = defaultdict(lambda: 0, json.loads(fileFfa.readline()))
# ffaArray3 = {int(k): int(v) for k, v in ffaArray3.items()}
# title2 = instanceName + "(" + str(10) + " machines and " + str(30) + " jobs)"
#
# instanceName = 'la35'
# fileName = resultFolder + instanceName + "/"
# fileFfa = open(fileName + 'ffaCompleteCurrent.txt')
# fileFfa.readline()
# ffaArray4 = defaultdict(lambda: 0, json.loads(fileFfa.readline()))
# ffaArray4 = {int(k): int(v) for k, v in ffaArray4.items()}
#
# fig, ((ax1, ax3), (ax2, ax4)) = plt.subplots(2, 2)
# ax1.bar(ffaArray1.keys(), ffaArray1.values(), 1000, label='FFA-Select')
# ax1.set_title(title1)
# ax2.bar(ffaArray2.keys(), ffaArray2.values(), 1000, color='orange', label='FFA-Complete')
# ax3.bar(ffaArray3.keys(), ffaArray3.values(), 1000)
# ax3.set_title(title2)
# ax4.bar(ffaArray4.keys(), ffaArray4.values(), 1000, color='orange')
# fig.text(0.5, 0.04, 'Objective Value', ha='center', fontsize=16)
# fig.text(0.04, 0.5, 'FFA Value', va='center', rotation='vertical', fontsize=16)
# handles1, labels1 = ax1.get_legend_handles_labels()
# handles2, labels2 = ax2.get_legend_handles_labels()
#
# handles = handles1 + handles2
# labels = labels1 + labels2
#
# fig.legend(handles, labels, loc=9)
# plt.show()
