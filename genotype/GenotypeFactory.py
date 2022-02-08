import random

from algorithm.Population import Population
from Config import Config
from genotype.SimpleEncoding import SimpleEncoding


class GenotypeFactory:

    @staticmethod
    def generateInitialSimpleEncoding():
        sequence = []
        for i in range(Config.jssp.amountJobs):
            for j in range(Config.jssp.amountMachines):
                sequence.append(i)
        return SimpleEncoding(sequence)

    @staticmethod
    def generateRandomSimpleEncodingFromSequence(sequence):
        randomSequence = random.sample(sequence, len(sequence))
        return SimpleEncoding(randomSequence)

    @staticmethod
    def generateRandomSimpleEncodingPopulationFromSequence(sequence, n):
        population = []
        for i in range(n):
            newEncoding = SimpleEncoding(random.sample(sequence, len(sequence)))
            population.append(newEncoding)
        return Population(population)

    @staticmethod
    def generateRandomSimpleEncoding():
        initialGenotype = GenotypeFactory.generateInitialSimpleEncoding()
        return GenotypeFactory.generateRandomSimpleEncodingFromSequence(initialGenotype.sequence)

    @staticmethod
    def generateRandomSimpleEncodingPopulation(n):
        initialGenotype = GenotypeFactory.generateInitialSimpleEncoding()
        return GenotypeFactory.generateRandomSimpleEncodingPopulationFromSequence(initialGenotype.sequence, n)
