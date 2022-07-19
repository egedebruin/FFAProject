import os
import sys

from Config import Config
from Experiments import Experiments
from Util import Util

if __name__ == '__main__':
    os.chdir(sys.argv[1])
    library = Util.readFullLibrary('files/jssp-instances/full_full_library.txt')

    for exponent in range(0, 2091):
        if int(1.01 ** exponent) not in Config.intermediateSavingList:
            Config.intermediateSavingList.append(int(1.01 ** exponent))

    Experiments.runPpaComparisonExperiment(library)