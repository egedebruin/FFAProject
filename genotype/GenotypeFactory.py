import random

from algorithm.Population import Population
from Config import Config
from genotype.SimpleEncoding import SimpleEncoding


class GenotypeFactory:

    @staticmethod
    def generateInitialSimpleEncoding(instance=None):
        jsspInstance = Config.jssp
        if instance is not None:
            jsspInstance = instance
        sequence = []
        for i in range(jsspInstance.amountJobs):
            for j in range(jsspInstance.amountMachines):
                sequence.append(i)
        return SimpleEncoding(sequence, instance)

    @staticmethod
    def generateRandomSimpleEncodingFromSequence(sequence):
        randomSequence = random.sample(sequence, len(sequence))
        return SimpleEncoding(randomSequence)

    @staticmethod
    def generateRandomSimpleEncodingPopulationFromSequence(sequence, n, instance=None):
        population = []
        for i in range(n):
            newEncoding = SimpleEncoding(random.sample(sequence, len(sequence)), instance)
            population.append(newEncoding)
        return Population(population)

    @staticmethod
    def generateRandomSimpleEncoding():
        initialGenotype = GenotypeFactory.generateInitialSimpleEncoding()
        return GenotypeFactory.generateRandomSimpleEncodingFromSequence(initialGenotype.sequence)

    @staticmethod
    def generateRandomSimpleEncodingPopulation(n, instance=None):
        initialGenotype = GenotypeFactory.generateInitialSimpleEncoding(instance)
        return GenotypeFactory.generateRandomSimpleEncodingPopulationFromSequence(initialGenotype.sequence, n, instance)
