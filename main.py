import json
from time import sleep

from Config import Config
from Experiments import Experiments
from Util import Util
from jssp.JSSPFactory import JSSPFactory
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd

# Get JSSP instance
# simpleFile = Util.readSimpleFile('files/jssp-instances/easy_jssp.txt')

if __name__ == '__main__':
    os.chdir(sys.argv[1])
    library = Util.readFullLibrary('files/jssp-instances/full_full_library.txt')

    Experiments.runHillClimberComparisonExperiment(library)

# populationFolder = 'files/output/hc/populations/1/'
#
# for subFolder in os.listdir(populationFolder):
#     hcFile = open(populationFolder + subFolder + '/hc.txt')
#     ffaFile = open(populationFolder + subFolder + '/fhc.txt')
#
#     hcLength = len(hcFile.read().split(','))
#     ffaLength = len(ffaFile.read().split(','))
#
#     if hcLength != ffaLength:
#         print(subFolder)
#         print(hcLength)
#         print(ffaLength)


# resultFolder = 'files/output/hc/results/1/'
# resultDict = {}
# hcBetter = 0
# ffaBetter = 0
# ties = 0
# totalRatio = 0
# hcJobs = 0
# hcMachines = 0
# ffaJobs = 0
# ffaMachines = 0
# tiesJobs = 0
# tiesMachines = 0
# allDict = {'instance': [],
#            'jobs': [],
#            'machines': [],
#            'hill climber': [],
#            'ffa': []}
# for subFolder in os.listdir(resultFolder):
#     jssp = JSSPFactory.generateJSSPFromFormat(library[subFolder])
#     if not os.path.exists(resultFolder + subFolder + "/fhc.txt"):
#         continue
#     hcFile = open(resultFolder + subFolder + "/hc.txt")
#     ffaFile = open(resultFolder + subFolder + "/fhc.txt")
#     hcResult = int(hcFile.read())
#     ffaResult = int(ffaFile.read())
#
#     ratio = ffaResult / hcResult
#     totalRatio += ratio
#     resultDict[subFolder] = ratio
#
#     if ratio == 1:
#         ties += 1
#         tiesJobs += jssp.amountJobs
#         tiesMachines += jssp.amountMachines
#     if ratio < 1:
#         ffaBetter += 1
#         ffaJobs += jssp.amountJobs
#         ffaMachines += jssp.amountMachines
#     if ratio > 1:
#         hcBetter += 1
#         hcJobs += jssp.amountJobs
#         hcMachines += jssp.amountMachines
#
#     allDict['instance'].append(subFolder)
#     allDict['jobs'].append(jssp.amountJobs)
#     allDict['machines'].append(jssp.amountMachines)
#     allDict['hill climber'].append(hcResult)
#     allDict['ffa'].append(ffaResult)
#
# df = pd.DataFrame(allDict)
# df.to_csv('allResults.csv', index=False)

#
# print(tiesMachines/38)
# print(tiesJobs/38)
# print(ffaMachines/82)
# print(ffaJobs/82)
# print(hcMachines/112)
# print(hcJobs/112)

# ffaBest = 'orb03, swv05, dmu50'
# hcBest = 'dmu80, dmu79, dmu76'
#
# fileName = 'files/output/hc/populations/1/ta80/'
# fileHC = open(fileName + 'hc.txt')
# fileFHC = open(fileName + 'fhc.txt')
#
# intermediateResultsHC = list(map(int, fileHC.readline().split(', ')[:-2]))
# intermediateResultsFHC = list(map(int, fileFHC.readline().split(', ')[:-1]))
# intermediateResultsHC.insert(0, None)
#
# xAxis = []
# for i in range(len(intermediateResultsHC)):
#     xAxis.append((i * 1000) + 1)
#
# plt.plot(xAxis, intermediateResultsHC, label='Hill Climber')
# plt.plot(xAxis, intermediateResultsFHC, label='FFA')
# plt.xscale('log')
# plt.legend()
# plt.xlabel('Function Evaluations')
# plt.ylabel('Objective Value (Execution time)')
# plt.title('orb02 (10 machines and 10 jobs)')
# plt.show()

# Experiments.runComparisonExperiment(library)

# Config.jssp = JSSPFactory.generateJSSPFromFormat(library['abz5'])
# Config.jssp = JSSPFactory.generateJSSPRandom(10, 10, 'uniform')

# Run algorithm
# Algorithm.memeticAlgorithm()

# Run experiments
# allTimes, bestInstance, bestTime = Experiments.doRandomExperiments(1)

# Show plots
# Util.showTimeHistogram(allTimes)
# Util.showGanttChart(bestInstance, Config.jssp.amountJobs)

# TODO: Read results
# TODO: Read more information and do something with it
