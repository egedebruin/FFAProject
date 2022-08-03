import os
import random

from Config import Config
from algorithm.Algorithm import Algorithm
from genotype.GenotypeFactory import GenotypeFactory
from genotype.SimpleEncoding import SimpleEncoding


class PpaAlgorithm:

    @staticmethod
    def ppaAlgorithm(instance, name, run, restartConfig):
        bestFileName = '/ppaAllBest.txt'
        currentFileName = '/ppaCurrent.txt'
        allPopFileName = '/ppaAllPop.txt'

        functionEvaluations = Config.populationSize
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(Config.populationSize, instance)
        best = population.selectBest([], 1)[0]

        if restartConfig.reset:
            functionEvaluations = restartConfig.functionEvaluations
            population.fromIndividualSequenceList(restartConfig.currentPopulation, instance)
            best = population.selectBest([], 1)[0]
        else:
            Algorithm.writeCurrentPopulationToFile(name, run, currentFileName, functionEvaluations, population)
            PpaAlgorithm.writeBestToFile(name, run, functionEvaluations, best.getObjectiveValue(), bestFileName)
            PpaAlgorithm.writeCurrentPopulationToAllFile(name, run, functionEvaluations, population, allPopFileName)

        previousEvaluations = functionEvaluations
        while functionEvaluations < Config.maxFunctionEvaluations:
            if functionEvaluations % 1000000 == 0 or (previousEvaluations % 1000000 > functionEvaluations % 1000000):
                print("PPA: On function evaluation " + str(
                    functionEvaluations) + " for instance " + name + " in run " + str(run))
            previousEvaluations = functionEvaluations

            minimumObjectiveValue, maximumObjectiveValue = population.getMinimumAndMaximumObjectiveValue()

            offspring = PpaAlgorithm.ppaGenerateOffspring(population, minimumObjectiveValue, maximumObjectiveValue,
                                                          instance)

            population.individuals = population.selectBest(offspring, Config.populationSize)
            best = population.selectBest([best], 1)[0]

            functionEvaluations += len(offspring)

            if functionEvaluations < 1000 or \
                    PpaAlgorithm.testMethod(previousEvaluations, functionEvaluations, 1000, 1000000) or \
                    PpaAlgorithm.testMethod(previousEvaluations, functionEvaluations, 1000000, 100000000) or \
                    PpaAlgorithm.testMethod(previousEvaluations, functionEvaluations, 100000000, 2000000000):
                Algorithm.writeCurrentPopulationToFile(name, run, currentFileName, functionEvaluations, population)
                PpaAlgorithm.writeBestToFile(name, run, functionEvaluations, best.getObjectiveValue(), bestFileName)
                PpaAlgorithm.writeCurrentPopulationToAllFile(name, run, functionEvaluations, population, allPopFileName)

            if PpaAlgorithm.testMethod(previousEvaluations, functionEvaluations, 1000000, 2000000000):
                Algorithm.writeCurrentPopulationToFile(name, run, currentFileName, functionEvaluations, population)

        Algorithm.writeCurrentPopulationToFile(name, run, currentFileName, functionEvaluations, population)
        PpaAlgorithm.writeBestToFile(name, run, functionEvaluations, best.getObjectiveValue(), bestFileName)
        PpaAlgorithm.writeCurrentPopulationToAllFile(name, run, functionEvaluations, population, allPopFileName)
        return best

    @staticmethod
    def ppaAlgorithmFFASelection(instance, name, run, restartConfig):
        bestFileName = '/ffaSelectAllBest.txt'
        currentFileName = '/ffaSelectCurrent.txt'
        allPopFileName = '/ffaSelectAllPop.txt'

        functionEvaluations = Config.populationSize
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(Config.populationSize, instance)
        best = population.selectBest([], 1)[0]

        if restartConfig.reset:
            functionEvaluations = restartConfig.functionEvaluations
            population.fromIndividualSequenceList(restartConfig.currentPopulation, instance)
            best = SimpleEncoding(restartConfig.currentBest, instance)
            population.frequency = restartConfig.frequencyTable
        else:
            Algorithm.writeCurrentPopulationToFile(name, run, currentFileName, functionEvaluations, population, population.frequency, best.sequence)
            PpaAlgorithm.writeBestToFile(name, run, functionEvaluations, best.getObjectiveValue(), bestFileName)
            PpaAlgorithm.writeCurrentPopulationToAllFile(name, run, functionEvaluations, population, allPopFileName)

        previousEvaluations = functionEvaluations
        while functionEvaluations < Config.maxFunctionEvaluations:
            if functionEvaluations % 1000000 == 0 or (previousEvaluations % 1000000 > functionEvaluations % 1000000):
                print("FFASelect: On function evaluation " + str(
                    functionEvaluations) + " for instance " + name + " in run " + str(run))
            previousEvaluations = functionEvaluations

            minimumObjectiveValue, maximumObjectiveValue = population.getMinimumAndMaximumObjectiveValue()

            offspring = PpaAlgorithm.ppaGenerateOffspring(population, minimumObjectiveValue, maximumObjectiveValue,
                                                          instance)

            population.individuals = population.selectLeastFrequent(offspring, Config.populationSize)
            best = population.selectBest([best], 1)[0]

            functionEvaluations += len(offspring)

            if functionEvaluations < 1000 or \
                    PpaAlgorithm.testMethod(previousEvaluations, functionEvaluations, 1000, 1000000) or \
                    PpaAlgorithm.testMethod(previousEvaluations, functionEvaluations, 1000000, 100000000) or \
                    PpaAlgorithm.testMethod(previousEvaluations, functionEvaluations, 100000000, 2000000000):
                Algorithm.writeCurrentPopulationToFile(name, run, currentFileName, functionEvaluations, population, population.frequency, best.sequence)
                PpaAlgorithm.writeBestToFile(name, run, functionEvaluations, best.getObjectiveValue(), bestFileName)
                PpaAlgorithm.writeCurrentPopulationToAllFile(name, run, functionEvaluations, population, allPopFileName)

            if PpaAlgorithm.testMethod(previousEvaluations, functionEvaluations, 1000000, 2000000000):
                Algorithm.writeCurrentPopulationToFile(name, run, currentFileName, functionEvaluations, population,
                                                       population.frequency, best.sequence)

        Algorithm.writeCurrentPopulationToFile(name, run, currentFileName, functionEvaluations, population,
                                               population.frequency, best.sequence)
        PpaAlgorithm.writeBestToFile(name, run, functionEvaluations, best.getObjectiveValue(), bestFileName)
        PpaAlgorithm.writeCurrentPopulationToAllFile(name, run, functionEvaluations, population, allPopFileName)
        return best

    @staticmethod
    def ppaAlgorithmFFAComplete(instance, name, run, restartConfig):
        bestFileName = '/ffaCompleteAllBest.txt'
        currentFileName = '/ffaCompleteCurrent.txt'
        allPopFileName = '/ffaCompleteAllPop.txt'

        functionEvaluations = Config.populationSize
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(Config.populationSize, instance)
        best = population.selectBest([], 1)[0]

        if restartConfig.reset:
            functionEvaluations = restartConfig.functionEvaluations
            population.fromIndividualSequenceList(restartConfig.currentPopulation, instance)
            best = SimpleEncoding(restartConfig.currentBest, instance)
            population.frequency = restartConfig.frequencyTable
        else:
            Algorithm.writeCurrentPopulationToFile(name, run, currentFileName, functionEvaluations, population, population.frequency, best.sequence)
            PpaAlgorithm.writeBestToFile(name, run, functionEvaluations, best.getObjectiveValue(), bestFileName)
            PpaAlgorithm.writeCurrentPopulationToAllFile(name, run, functionEvaluations, population, allPopFileName)

        previousEvaluations = functionEvaluations
        while functionEvaluations < Config.maxFunctionEvaluations:
            if functionEvaluations % 1000000 == 0 or (previousEvaluations % 1000000 > functionEvaluations % 1000000):
                print("FFAComplete: On function evaluation " + str(functionEvaluations) + " for instance " + name + " in run " + str(run))
            previousEvaluations = functionEvaluations

            minimumObjectiveValue, maximumObjectiveValue = population.getMinimumAndMaximumFFAValue()

            offspring = PpaAlgorithm.ppaGenerateOffspring(population, minimumObjectiveValue, maximumObjectiveValue,
                                                          instance, True)

            population.individuals = population.selectLeastFrequent(offspring, Config.populationSize)
            best = population.selectBest([best], 1)[0]

            functionEvaluations += len(offspring)

            if functionEvaluations < 1000 or \
                    PpaAlgorithm.testMethod(previousEvaluations, functionEvaluations, 1000, 1000000) or \
                    PpaAlgorithm.testMethod(previousEvaluations, functionEvaluations, 1000000, 100000000) or \
                    PpaAlgorithm.testMethod(previousEvaluations, functionEvaluations, 100000000, 2000000000):
                Algorithm.writeCurrentPopulationToFile(name, run, currentFileName, functionEvaluations, population, population.frequency, best.sequence)
                PpaAlgorithm.writeBestToFile(name, run, functionEvaluations, best.getObjectiveValue(), bestFileName)
                PpaAlgorithm.writeCurrentPopulationToAllFile(name, run, functionEvaluations, population, allPopFileName)

            if PpaAlgorithm.testMethod(previousEvaluations, functionEvaluations, 1000000, 2000000000):
                Algorithm.writeCurrentPopulationToFile(name, run, currentFileName, functionEvaluations, population,
                                                       population.frequency, best.sequence)

        Algorithm.writeCurrentPopulationToFile(name, run, currentFileName, functionEvaluations, population,
                                               population.frequency, best.sequence)
        PpaAlgorithm.writeBestToFile(name, run, functionEvaluations, best.getObjectiveValue(), bestFileName)
        PpaAlgorithm.writeCurrentPopulationToAllFile(name, run, functionEvaluations, population, allPopFileName)
        return best

    @staticmethod
    def testMethod(previousEvaluations, functionEvaluations, modulo, threshold):
        if (functionEvaluations < threshold) & (previousEvaluations % modulo >= functionEvaluations % modulo):
            return True
        return False

    @staticmethod
    def ppaGenerateOffspring(population, minimumObjectiveValue, maximumObjectiveValue, instance, ffa=False):
        offspring = []
        for individual in population.individuals:
            objectiveValue = individual.getObjectiveValue()
            if ffa:
                objectiveValue = population.frequency[objectiveValue]
            fitnessValue = individual.getPpaFitnessValue(minimumObjectiveValue, maximumObjectiveValue, objectiveValue)
            amountOffspring, amountSwaps = PpaAlgorithm.ppaGetAmountOffspringAndSwaps(fitnessValue, instance)

            for i in range(int(amountOffspring)):
                newIndividual = PpaAlgorithm.nRandomSwap(amountSwaps, individual, instance)
                offspring.append(newIndividual)
        return offspring

    @staticmethod
    def nRandomSwap(amountSwaps, individual, instance):
        newIndividual = SimpleEncoding(individual.sequence, instance)
        for i in range(int(amountSwaps)):
            newIndividual.randomSingleSwap(True)
        return newIndividual

    @staticmethod
    def ppaGetAmountOffspringAndSwaps(fitnessValue, instance):
        maxAmountSwaps = 0.5 * (instance.amountJobs * instance.amountMachines)
        amountOffspring = max(1, Config.maxOffspring * fitnessValue * random.random())
        amountSwaps = max(1, maxAmountSwaps * random.random() * (1 - fitnessValue))

        return amountOffspring, amountSwaps

    @staticmethod
    def writeBestToFile(name, run, functionEvaluations, value, endFileName):
        fileName = str(run) + "/" + name + endFileName

        os.makedirs(os.path.dirname(Config.intermediateFolder + fileName), exist_ok=True)
        populationsWriteFile = open(Config.intermediateFolder + fileName, 'a')
        populationsWriteFile.write(str(functionEvaluations) + ":" + str(value) + ", ")

    @staticmethod
    def writeCurrentPopulationToAllFile(name, run, functionEvaluations, population, endFileName):
        fileName = str(run) + "/" + name + endFileName

        os.makedirs(os.path.dirname(Config.intermediateFolder + fileName), exist_ok=True)
        populationsWriteFile = open(Config.intermediateFolder + fileName, 'a')
        populationsWriteFile.write(str(functionEvaluations) + ":" + str(population.getObjectiveValuesList()) + "; ")
