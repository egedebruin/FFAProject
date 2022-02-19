from time import sleep

from Config import Config
from algorithm.Algorithm import Algorithm
from genotype.GenotypeFactory import GenotypeFactory
from jssp.JSSPFactory import JSSPFactory
from multiprocessing import Process
from multiprocessing import Pool
import pandas as pd
import os


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
    def runHillClimberComparisonExperiment(library):
        for i in range(Config.runs):
            pool = Pool(processes=100)
            run = i + 1
            print("Starting experiment run: " + str(run))
            print("-----")

            for name, instanceFormat in library.items():
                instance = JSSPFactory.generateJSSPFromFormat(instanceFormat)
                if not os.path.exists('files/output/hc/results/' + str(run) + "/" + name + "/hc.txt"):
                    pool.apply_async(Experiments.runHillClimberAlgorithm, args=(False, name, instance, run))
                if not os.path.exists('files/output/hc/results/' + str(run) + "/" + name + "/fhc.txt"):
                    pool.apply_async(Experiments.runHillClimberAlgorithm, args=(True, name, instance, run))
            pool.close()
            pool.join()

    @staticmethod
    def runHillClimberAlgorithm(ffa, instanceName, instance, run):
        if ffa:
            print("Running FFA algorithm " + instanceName)
            allPopulations, best = Algorithm.frequencyAssignmentHillClimberAlgorithm(instance, instanceName, run)
            fileName = str(run) + "/" + instanceName + "/fhc.txt"
            print("FFA algorithm " + instanceName + " done!")
        else:
            print("Running normal algorithm " + instanceName)
            allPopulations, best = Algorithm.hillClimberAlgorithm(instance)
            fileName = str(run) + "/" + instanceName + "/hc.txt"
            print("Normal algorithm " + instanceName + " done!")

        os.makedirs(os.path.dirname('files/output/hc/populations/' + fileName), exist_ok=True)
        populationsWriteFile = open('files/output/hc/populations/' + fileName, 'w')
        populationsWriteFile.write("\n".join(allPopulations))

        os.makedirs(os.path.dirname('files/output/hc/results/' + fileName), exist_ok=True)
        resultsWriteFile = open('files/output/hc/results/' + fileName, 'w')
        resultsWriteFile.write(str(int(best.getObjectiveValue())))

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
        os.makedirs(os.path.dirname('files/output/populations/' + str(run) + "/" + instanceName + "/placeholder.txt"), exist_ok=True)
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
