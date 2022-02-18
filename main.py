from Config import Config
from Experiments import Experiments
from Util import Util
from algorithm.Algorithm import Algorithm
from jssp.JSSPFactory import JSSPFactory


# Get JSSP instance
# simpleFile = Util.readSimpleFile('files/jssp-instances/easy_jssp.txt')

library = Util.readFullLibrary('files/jssp-instances/full_library.txt')

Experiments.runComparisonExperiment(library)

# Config.jssp = JSSPFactory.generateJSSPFromFormat(library['abz5'])
# Config.jssp = JSSPFactory.generateJSSPRandom(10, 10, 'uniform')

# Run algorithm
# Algorithm.memeticAlgorithm()
# Algorithm.hillClimberAlgorithm()
# Run experiments
# allTimes, bestInstance, bestTime = Experiments.doRandomExperiments(1)

# Show plots
# Util.showTimeHistogram(allTimes)
# Util.showGanttChart(bestInstance, Config.jssp.amountJobs)

# TODO: Read results
# TODO: Read more information and do something with it
