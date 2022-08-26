from Config import Config
from algorithm.Algorithm import Algorithm
from algorithm.PpaAlgorithm import PpaAlgorithm
from algorithm.RestartConfig import RestartConfig
from genotype.GenotypeFactory import GenotypeFactory
from jssp.JSSPFactory import JSSPFactory
from multiprocessing import Pool
import pandas as pd
import os
import json
import itertools
from filelock import FileLock
from collections import defaultdict


class Experiments:

    @staticmethod
    def doRandomExperiments(amountExperiments):
        print("Starting experiments")
        initialGenotype = GenotypeFactory.generateInitialSimpleEncoding()

        bestExecutionTime = float('inf')
        bestPhenotype = None
        executionTimes = []
        for i in range(amountExperiments):
            if i % 10000 == 0:
                print("Doing experiment number: " + str(i))

            randomGenotype = GenotypeFactory.generateRandomSimpleEncoding()

            phenotype = randomGenotype.toPhenotype()
            executionTime = phenotype.getObjectiveValue()
            executionTimes.append(executionTime)

            if executionTime < bestExecutionTime:
                bestExecutionTime = executionTime
                bestPhenotype = phenotype

        print("Experiments finished")
        return executionTimes, bestPhenotype, bestExecutionTime

    @staticmethod
    def goThroughEntireSearchSpace():
        genotype = GenotypeFactory.generateInitialSimpleEncoding()
        permutations = list(itertools.permutations(genotype.sequence))
        best = 10000
        bestPhenotype = None

        for permutation in permutations:
            genotype.sequence = permutation
            genotype.objectiveValue = 0
            if genotype.getObjectiveValue() < best:
                print(genotype.sequence)
                print(genotype.getObjectiveValue())
                best = genotype.getObjectiveValue()
                bestPhenotype = genotype.toPhenotype()

        return bestPhenotype

    @staticmethod
    def runComparisonExperiment(library):
        results, run, currentInstance, correctRestart = Experiments.restartValues()

        while True:
            if run > Config.runs:
                break
            print("Starting experiment run: " + str(run))
            print("-----")
            for instanceName, instance in library.items():
                if not correctRestart:
                    if instanceName == currentInstance:
                        correctRestart = True
                    continue
                Config.jssp = JSSPFactory.generateJSSPFromFormat(instance)
                print("Running normal memetic algorithm " + instanceName)
                allPopulationsMA, bestMA = Algorithm.memeticAlgorithm()
                print("Running FFA memetic algorithm " + instanceName)
                allPopulationsFMA, bestFMA = Algorithm.frequencyAssignmentMemeticAlgorithm()

                results = results.append({'run': run, 'instance': instanceName,
                                          'bestFMA': int(bestFMA.getObjectiveValue()),
                                          'bestMA': int(bestMA.getObjectiveValue())},
                                         ignore_index=True)

                print("Instance with name " + instanceName + " done.")
                print("-----")
                Experiments.writeFiles(allPopulationsMA, allPopulationsFMA, results, instanceName, run)
            run += 1
            print("-----")

    @staticmethod
    def runHillClimberComparisonExperiment(library, sortedInstances):
        pool = Pool(processes=Config.poolProcesses)
        for name, size in sortedInstances.items():
            instanceFormat = library[name]

            for i in range(Config.runs):
                run = i + 1
                instance = JSSPFactory.generateJSSPFromFormat(instanceFormat)
                if not os.path.exists(Config.resultFolder + str(run) + "/" + name + "/hc.txt"):
                    pool.apply_async(Experiments.runHillClimberAlgorithm, args=(name, instance, run))
                if not os.path.exists(Config.resultFolder + str(run) + "/" + name + "/fhc.txt"):
                    pool.apply_async(Experiments.runFFAHillClimberAlgorithm, args=(name, instance, run))

        pool.close()
        pool.join()

    @staticmethod
    def runHillClimberAlgorithm(instanceName, instance, run):
        if Experiments.instanceIsTaken(instanceName, 'hc', run):
            return
        print("Running normal algorithm " + instanceName + " run " + str(run))
        restartConfig = RestartConfig()
        restartConfig.setRestartValuesNormalHillClimber(instanceName, run)
        best = Algorithm.hillClimberAlgorithm(instance, instanceName, run, restartConfig)
        best = best.getObjectiveValue()
        fileName = str(run) + "/" + instanceName + "/hc.txt"
        print("Normal algorithm " + instanceName + " run " + str(run) + " done!")

        Experiments.writeBestResults(fileName, best)

    @staticmethod
    def runFFAHillClimberAlgorithm(instanceName, instance, run):
        if Experiments.instanceIsTaken(instanceName, 'ffa', run):
            return
        print("Running FFA algorithm " + instanceName + " run " + str(run))
        restartConfig = RestartConfig()
        restartConfig.setRestartValuesFFAHillClimber(instanceName, run)
        best = Algorithm.frequencyAssignmentHillClimberAlgorithm(instance, instanceName, run, restartConfig)
        best = best.getObjectiveValue()
        fileName = str(run) + "/" + instanceName + "/fhc.txt"
        print("FFA algorithm " + instanceName + " run " + str(run))

        Experiments.writeBestResults(fileName, best)

    @staticmethod
    def runPpaComparisonExperiment(library):
        for i in range(Config.runs):
            pool = Pool(processes=Config.poolProcesses)
            run = i + 1
            print("Starting experiment run: " + str(run))
            print("-----")

            for name, instanceFormat in library.items():
                instance = JSSPFactory.generateJSSPFromFormat(instanceFormat)
                if not os.path.exists(Config.resultFolder + str(run) + "/" + name + "/ppa.txt"):
                    pool.apply_async(Experiments.runPpaAlgorithm, args=(name, instance, run))
                if not os.path.exists(Config.resultFolder + str(run) + "/" + name + "/ffaSelectPpa.txt"):
                    pool.apply_async(Experiments.runPpaFfaSelectAlgorithm, args=(name, instance, run))
                if not os.path.exists(Config.resultFolder + str(run) + "/" + name + "/ffaCompletePpa.txt"):
                    pool.apply_async(Experiments.runPpaFfaCompleteAlgorithm, args=(name, instance, run))
            pool.close()
            pool.join()

    @staticmethod
    def runPpaAlgorithm(instanceName, instance, run):
        if Experiments.instanceIsTaken(instanceName, 'ppa'):
            return
        print("Running ppa algorithm " + instanceName)
        restartConfig = RestartConfig()
        restartConfig.setRestartValuesPpa(instanceName, run, '/ppaCurrent.txt')
        best = PpaAlgorithm.ppaAlgorithm(instance, instanceName, run, restartConfig)
        best = best.getObjectiveValue()
        fileName = str(run) + "/" + instanceName + "/ppa.txt"
        print("Ppa algorithm " + instanceName + " done!")

        Experiments.writeBestResults(fileName, best)

    @staticmethod
    def runPpaFfaSelectAlgorithm(instanceName, instance, run):
        if Experiments.instanceIsTaken(instanceName, 'ffaSelect'):
            return
        print("Running ffaSelect algorithm " + instanceName)
        restartConfig = RestartConfig()
        restartConfig.setRestartValuesPpa(instanceName, run, '/ffaSelectCurrent.txt')
        best = PpaAlgorithm.ppaAlgorithmFFASelection(instance, instanceName, run, restartConfig)
        best = best.getObjectiveValue()
        fileName = str(run) + "/" + instanceName + "/ffaSelectPpa.txt"
        print("FfaSelect algorithm " + instanceName + " done!")

        Experiments.writeBestResults(fileName, best)

    @staticmethod
    def runPpaFfaCompleteAlgorithm(instanceName, instance, run):
        if Experiments.instanceIsTaken(instanceName, 'ffaComplete'):
            return
        print("Running ffaComplete algorithm " + instanceName)
        restartConfig = RestartConfig()
        restartConfig.setRestartValuesPpa(instanceName, run, '/ffaCompleteCurrent.txt')
        best = PpaAlgorithm.ppaAlgorithmFFAComplete(instance, instanceName, run, restartConfig)
        best = best.getObjectiveValue()
        fileName = str(run) + "/" + instanceName + "/ffaCompletePpa.txt"
        print("FfaComplete algorithm " + instanceName + " done!")

        Experiments.writeBestResults(fileName, best)

    @staticmethod
    def writeBestResults(fileName, best):
        os.makedirs(os.path.dirname(Config.resultFolder + fileName), exist_ok=True)
        resultsWriteFile = open(Config.resultFolder + fileName, 'w')
        resultsWriteFile.write(str(int(best)))

    @staticmethod
    def restartValues():
        run = 1
        correctRestart = True
        currentInstance = None
        results = pd.DataFrame()
        if os.path.isfile('files/output/results.csv'):
            results = pd.read_csv('files/output/results.csv')
            run = results['run'].iloc[-1]
            currentInstance = results['instance'].iloc[-1]
            correctRestart = False

        return results, int(run), currentInstance, correctRestart

    @staticmethod
    def writeFiles(allPopulationsMA, allPopulationsFMA, dataFrame, instanceName, run):
        os.makedirs(os.path.dirname('files/output/populations/' + str(run) + "/" + instanceName + "/placeholder.txt"),
                    exist_ok=True)
        maWriteFile = open('files/output/populations/' + str(run) + "/" + instanceName + "/maPopulations.txt",
                           'w')
        maWriteFile.write("\n".join(allPopulationsMA))
        fmaWriteFile = open('files/output/populations/' + str(run) + "/" + instanceName + "/fmaPopulations.txt",
                            'w')
        fmaWriteFile.write("\n".join(allPopulationsFMA))

        dataFrame['run'] = dataFrame['run'].astype('int')
        dataFrame['bestFMA'] = dataFrame['bestFMA'].astype('int')
        dataFrame['bestMA'] = dataFrame['bestMA'].astype('int')
        dataFrame.to_csv('files/output/results.csv', index=False)

    @staticmethod
    def instanceIsTaken(instanceName, algorithmType, run=1):
        with FileLock('files/taken.txt.lock'):
            file = open('files/taken.txt', 'r')
            if instanceName + algorithmType + str(run) in file.read():
                file.close()
                return True
            file.close()

            file = open('files/taken.txt', 'a')
            file.write(', ' + instanceName + algorithmType + str(run))
            file.close()
            return False
