from Config import Config
from Experiments import Experiments
from Util import Util
from algorithm.Algorithm import Algorithm
from jssp.JSSPFactory import JSSPFactory
import threading


# Get JSSP instance
# simpleFile = Util.readSimpleFile('files/jssp-instances/easy_jssp.txt')

library = Util.readFullLibrary('files/jssp-instances/full_library.txt')

# Experiments.runComparisonExperiment(library)

Config.jssp = JSSPFactory.generateJSSPFromFormat(library['abz5'])
# Config.jssp = JSSPFactory.generateJSSPRandom(10, 10, 'uniform')

# Run algorithm
# Algorithm.memeticAlgorithm()
x = threading.Thread(target=Algorithm.hillClimberAlgorithm, args=(1,))
y = threading.Thread(target=Algorithm.hillClimberAlgorithm, args=(2,))

x.start()
y.start()
# Run experiments
# allTimes, bestInstance, bestTime = Experiments.doRandomExperiments(1)

# Show plots
# Util.showTimeHistogram(allTimes)
# Util.showGanttChart(bestInstance, Config.jssp.amountJobs)

# TODO: Read results
# TODO: Read more information and do something with it
