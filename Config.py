class Config:
    jssp = None
    populationSize = 30
    offspringSize = 16
    maxOffspring = 5
    # TODO: Think of good populationSize and maxOffspring
    amountBitSwaps = 10
    runs = 1
    timePerRun = 300
    maxFunctionEvaluations = 2 ** 30
    poolProcesses = 1
    resultFolder = 'files/output/ppa/results/'
    intermediateFolder = 'files/output/ppa/populations/'
