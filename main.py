import os
import sys

from Experiments import Experiments
from Util import Util

if __name__ == '__main__':
    os.chdir(sys.argv[1])
    library = Util.readFullLibrary('files/jssp-instances/full_full_library.txt')

    Experiments.runHillClimberComparisonExperiment(library)
