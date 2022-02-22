import os

from Config import Config
from genotype.GenotypeFactory import GenotypeFactory
import time


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
    def hillClimberAlgorithm(instance, name, run):
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(1, instance)
        best = population.individuals[0]
        functionEvaluations = 1

        while functionEvaluations < Config.maxFunctionEvaluations:
            if functionEvaluations % 1000000 == 0:
                print("Normal: On function evaluation " + str(functionEvaluations) + " for instance " + name + " in run " + str(run))
            newIndividual = population.individuals[0].randomSingleSwap()

            best = population.selectBest([best, newIndividual], 1)[0]
            if functionEvaluations % 1000 == 0:
                Algorithm.writeBestToFile(name, run, best.getObjectiveValue(), False)

            population.individuals = population.selectBestPreferOffspring([newIndividual])

            functionEvaluations += 1

        return best

    @staticmethod
    def frequencyAssignmentHillClimberAlgorithm(instance, name, run):
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(1, instance)
        best = population.individuals[0]
        functionEvaluations = 1

        while functionEvaluations < Config.maxFunctionEvaluations:
            if functionEvaluations % 1000000 == 0:
                print("FFA: On function evaluation " + str(functionEvaluations) + " for instance " + name + " in run " + str(run))
            newIndividual = population.individuals[0].randomSingleSwap()

            best = population.selectBest([best, newIndividual], 1)[0]
            if functionEvaluations % 1000 == 0:
                Algorithm.writeBestToFile(name, run, best.getObjectiveValue(), True)

            population.individuals = population.selectLeastFrequentPreferOffspring([newIndividual])

            functionEvaluations += 1

        return best

    @staticmethod
    def writeBestToFile(name, run, value, ffa):
        if ffa:
            fileName = str(run) + "/" + name + "/fhc.txt"
        else:
            fileName = str(run) + "/" + name + "/hc.txt"

        os.makedirs(os.path.dirname('files/output/hc/populations/' + fileName), exist_ok=True)
        populationsWriteFile = open('files/output/hc/populations/' + fileName, 'a')
        populationsWriteFile.write(str(value) + ", ")
