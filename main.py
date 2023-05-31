import os
import sys

from Config import Config
from Experiments import Experiments
import operator
from Util import Util
from jssp.JSSPFactory import JSSPFactory

if __name__ == '__main__':
    os.chdir(sys.argv[1])
    library = Util.readFullLibrary(Config.libraryFile)

    result = {}
    for name, instanceFormat in library.items():
        instance = JSSPFactory.generateJSSPFromFormat(instanceFormat)
        size = instance.amountJobs * instance.amountMachines
        result[name] = size
    sortedInstances = dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True))

    Experiments.runPpaComparisonExperiment(library, sortedInstances)
    #Experiments.runHillClimberComparisonExperiment(library, sortedInstances)
