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
    def hillClimberAlgorithm():
        allPopulations = []
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(1)
        best = population.individuals[0]
        allPopulations.append(population.getIndividualsStringSingleIndividual())
        functionEvaluations = 1

        while functionEvaluations < Config.maxFunctionEvaluations:
            if functionEvaluations % 10000 == 0:
                print(Config.timeThingy)
                Config.timeThingy = 0
            currentTime = time.time()
            newIndividual = population.individuals[0].randomSingleSwap()

            best = population.selectBest([best, newIndividual], 1)[0]

            population.individuals = population.selectBestPreferOffspring([newIndividual])
            allPopulations.append(population.getIndividualsStringSingleIndividual())

            functionEvaluations += 1
            Config.timeThingy += time.time() - currentTime

        return allPopulations, best

    @staticmethod
    def frequencyAssignmentHillClimberAlgorithm():
        allPopulations = []
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(1)
        best = population.individuals[0]
        allPopulations.append(population.getIndividualsStringSingleIndividual())
        functionEvaluations = 1

        while functionEvaluations < Config.maxFunctionEvaluations:
            newIndividual = population.individuals[0].randomSingleSwap()

            best = population.selectBest([best, newIndividual], 1)[0]

            population.individuals = population.selectLeastFrequentPreferOffspring([newIndividual])
            allPopulations.append(population.getIndividualsStringSingleIndividual())

            functionEvaluations += 1

        return allPopulations, best
