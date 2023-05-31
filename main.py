import os
import sys
import signal

from Config import Config
from Experiments import Experiments
import operator
from Util import Util
from jssp.JSSPFactory import JSSPFactory


class TimeOutException(Exception):
    pass


def alarm_handler(signum, frame):
    raise TimeOutException()


if __name__ == '__main__':
    os.chdir(sys.argv[1])
    library = Util.readFullLibrary(Config.libraryFile)

    result = {}
    for name, instanceFormat in library.items():
        instance = JSSPFactory.generateJSSPFromFormat(instanceFormat)
        size = instance.amountJobs * instance.amountMachines
        result[name] = size
    sortedInstances = dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True))

    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm((60 * 60 * 24 * 5) - 60 * 15)

    try:
        Experiments.runPpaComparisonExperiment(library, sortedInstances)
        #Experiments.runHillClimberComparisonExperiment(library, sortedInstances)
    except TimeOutException as ex:
        print('Alarmed, we are done')
