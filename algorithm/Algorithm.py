import os

from Config import Config
from genotype.GenotypeFactory import GenotypeFactory
import time
import json
import random

from genotype.SimpleEncoding import SimpleEncoding


class Algorithm:

    @staticmethod
    def memeticAlgorithm():
        allPopulations = []
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(Config.populationSize)
        best = population.selectBest([], 1)[0]
        allPopulations.append(population.getIndividualsString())

        startTime = time.time()
        while time.time() - startTime < Config.timePerRun:
            offspring = population.generateOffspring()
            population.individuals = population.selectBest(offspring, Config.populationSize)

            best = population.selectBest([best], 1)[0]
            allPopulations.append(population.getIndividualsString())

        return allPopulations, best

    @staticmethod
    def frequencyAssignmentMemeticAlgorithm():
        allPopulations = []
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(Config.populationSize)
        best = population.selectBest([], 1)[0]
        allPopulations.append(population.getIndividualsString())

        startTime = time.time()
        while time.time() - startTime < Config.timePerRun:
            offspring = population.generateOffspring()
            population.individuals = population.selectLeastFrequent(offspring, Config.populationSize)

            best = population.selectBest([best], 1)[0]
            allPopulations.append(population.getIndividualsString())

        return allPopulations, best

    @staticmethod
    def hillClimberAlgorithm(instance, name, run, restartConfig):
        bestFileName = '/hc.txt'
        currentPopulationFileName = '/current_hc.txt'

        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(1, instance)
        if restartConfig.currentPopulation is not None:
            population.individuals = [SimpleEncoding(restartConfig.currentPopulation, instance)]

        best = population.individuals[0]

        if restartConfig.currentPopulation is None:
            Algorithm.writeBestToFile(name, run, best.getObjectiveValue(), bestFileName)

        functionEvaluations = restartConfig.functionEvaluations
        while functionEvaluations < Config.maxFunctionEvaluations:
            if functionEvaluations % 1000000 == 0:
                print("Normal: On function evaluation " + str(functionEvaluations) + " for instance " + name + " in run " + str(run))
            newIndividual = population.individuals[0].randomSingleSwap()

            best = population.selectBest([best, newIndividual], 1)[0]

            population.individuals = population.selectBestPreferOffspring([newIndividual])

            functionEvaluations += 1
            if functionEvaluations % 1000 == 0:
                Algorithm.writeBestToFile(name, run, best, bestFileName)
                Algorithm.writeCurrentPopulationToFile(name, run, currentPopulationFileName, functionEvaluations,
                                                       population, population.frequency)

        return best

    @staticmethod
    def frequencyAssignmentHillClimberAlgorithm(instance, name, run, restartConfig):
        bestFileName = '/fhc.txt'
        currentPopulationFileName = '/current_fhc.txt'

        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(1, instance)
        if restartConfig.currentPopulation is not None:
            population.individuals = [SimpleEncoding(restartConfig.currentPopulation, instance)]

        if restartConfig.frequencyTable is not None:
            population.frequency = restartConfig.frequencyTable

        best = restartConfig.currentBest
        if restartConfig.currentBest == 0:
            best = population.individuals[0].getObjectiveValue()
            Algorithm.writeBestToFile(name, run, best, bestFileName)

        functionEvaluations = restartConfig.functionEvaluations

        while functionEvaluations < Config.maxFunctionEvaluations:
            if functionEvaluations % 1000000 == 0:
                print("FFA: On function evaluation " + str(functionEvaluations) + " for instance " + name + " in run " + str(run))
            newIndividual = population.individuals[0].randomSingleSwap()

            if newIndividual.getObjectiveValue() < best:
                best = newIndividual.getObjectiveValue()

            population.individuals = population.selectLeastFrequentPreferOffspring([newIndividual])

            functionEvaluations += 1
            if functionEvaluations % 1000 == 0:
                Algorithm.writeBestToFile(name, run, best, bestFileName)
                Algorithm.writeCurrentPopulationToFile(name, run, currentPopulationFileName, functionEvaluations, population, population.frequency)

        return best

    @staticmethod
    def writeBestToFile(name, run, value, endFileName):
        fileName = str(run) + "/" + name + endFileName

        os.makedirs(os.path.dirname(Config.intermediateFolder + fileName), exist_ok=True)
        populationsWriteFile = open(Config.intermediateFolder + fileName, 'a')
        populationsWriteFile.write(str(value) + ", ")

    @staticmethod
    def writeCurrentPopulationToFile(name, run, endFileName, evaluations, population, frequency=None, best=None):
        fileName = str(run) + "/" + name + endFileName
        text = str(evaluations) + ", " + population.getIndividualsString() + "\n" + json.dumps(frequency) + "\n" + str(best)

        os.makedirs(os.path.dirname(Config.intermediateFolder + fileName), exist_ok=True)
        populationsWriteFile = open(Config.intermediateFolder + fileName, 'w')
        populationsWriteFile.write(text)
