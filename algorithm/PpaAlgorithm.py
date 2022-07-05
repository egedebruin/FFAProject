import random

from Config import Config
from algorithm.Algorithm import Algorithm
from genotype.GenotypeFactory import GenotypeFactory


class PpaAlgorithm:

    @staticmethod
    def ppaAlgorithm(instance, name, run):
        # TODO: Intermediate file saving
        # TODO: Restart values
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(Config.populationSize, instance)
        best = population.selectBest([], 1)[0]

        functionEvaluations = Config.populationSize
        while functionEvaluations < Config.maxFunctionEvaluations:
            minimumObjectiveValue, maximumObjectiveValue = population.getMinimumAndMaximumObjectiveValue()

            offspring = PpaAlgorithm.ppaGenerateOffspring(population, minimumObjectiveValue, maximumObjectiveValue,
                                                          instance)

            population.individuals = population.selectBestPreferOffspring(offspring, Config.populationSize)
            best = population.selectBest(best, 1)[0]

            functionEvaluations += len(offspring)

        return best

    @staticmethod
    def ppaAlgorithmFFASelection(instance, name, run):
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(Config.populationSize, instance)
        best = population.selectBest([], 1)[0]

        functionEvaluations = Config.populationSize
        while functionEvaluations < Config.maxFunctionEvaluations:
            minimumObjectiveValue, maximumObjectiveValue = population.getMinimumAndMaximumObjectiveValue()

            offspring = PpaAlgorithm.ppaGenerateOffspring(population, minimumObjectiveValue, maximumObjectiveValue,
                                                          instance)

            population.individuals = population.selectLeastFrequentPreferOffspring(offspring, Config.populationSize)
            best = population.selectBest(best, 1)[0]

            functionEvaluations += len(offspring)

        return best

    @staticmethod
    def ppaAlgorithmFFAComplete(instance, name, run):
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(Config.populationSize, instance)
        best = population.selectBest([], 1)[0]

        functionEvaluations = Config.populationSize
        while functionEvaluations < Config.maxFunctionEvaluations:
            minimumObjectiveValue, maximumObjectiveValue = population.getMinimumAndMaximumFFAValue()

            offspring = PpaAlgorithm.ppaGenerateOffspring(population, minimumObjectiveValue, maximumObjectiveValue,
                                                          instance)

            population.individuals = population.selectLeastFrequentPreferOffspring(offspring, Config.populationSize)
            best = population.selectBest(best, 1)[0]

            functionEvaluations += len(offspring)

        return best

    @staticmethod
    def ppaGenerateOffspring(population, minimumObjectiveValue, maximumObjectiveValue, instance):
        offspring = []
        for individual in population.individuals:
            fitnessValue = individual.getPpaFitnessValueStandard(minimumObjectiveValue, maximumObjectiveValue)
            amountOffspring, amountSwaps = PpaAlgorithm.ppaGetAmountOffspringAndSwaps(fitnessValue, instance)

            for i in range(amountOffspring):
                newIndividual = Algorithm.nRandomSwap(amountSwaps, individual)
                offspring.append(newIndividual)
        return offspring

    @staticmethod
    def nRandomSwap(amountSwaps, individual):
        for i in range(amountSwaps):
            individual = individual.randomSingleSwap()
        return individual

    @staticmethod
    def ppaGetAmountOffspringAndSwaps(fitnessValue, instance):
        maxAmountSwaps = instance.amountJobs * instance.amountMachines
        # TODO: Think of good maxAmountSwaps
        amountOffspring = Config.maxOffspring * fitnessValue * random.random()
        amountSwaps = maxAmountSwaps * 2 * (1 - fitnessValue) * (random.random() - 0.5)

        return amountOffspring, amountSwaps
