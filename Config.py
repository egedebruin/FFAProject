class Config:
    jssp = None
    populationSize = 40
    offspringSize = 16
    maxOffspring = 10
    relativeMaxAmountSwaps = 0.5
    amountBitSwaps = 10
    runs = 1
    timePerRun = 300
    maxFunctionEvaluations = 2 ** 30
    poolProcesses = 16
    resultFolder = 'files/output/ppa2/results/'
    intermediateFolder = 'files/output/ppa2/populations/'
