from time import sleep

from Experiments import Experiments
from Util import Util
import matplotlib.pyplot as plt
import os
import sys

# Get JSSP instance
# simpleFile = Util.readSimpleFile('files/jssp-instances/easy_jssp.txt')

if __name__ == '__main__':
    os.chdir(sys.argv[1])
    library = Util.readFullLibrary('files/jssp-instances/full_full_library.txt')

    Experiments.runHillClimberComparisonExperiment(library)

# fileName = 'files/output/hc/populations/1/dmu25/'
# fileHC = open(fileName + 'hc.txt')
# fileFHC = open(fileName + 'fhc.txt')
#
# intermediateResultsHC = list(map(int, fileHC.readline().split(', ')[:-1]))
# intermediateResultsFHC = list(map(int, fileFHC.readline().split(', ')[:-1]))
#
# xAxis = []
# for i in range(len(intermediateResultsHC)):
#     xAxis.append((i+1) * 1000)
#
# plt.plot(xAxis, intermediateResultsHC)
# plt.plot(xAxis, intermediateResultsFHC)
# plt.xscale('log')
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
