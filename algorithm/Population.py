import random
import pandas as pd
import math
from collections import defaultdict

from Config import Config
from genotype.SimpleEncoding import SimpleEncoding


class Population:

    def __init__(self, population):
        self.individuals = population
        self.frequency = defaultdict(lambda: 0, {})

        for individual in self.individuals:
            self.updateFrequencyTable(individual)

    def generateOffspring(self):
        offspring = []
        for j in range(Config.offspringSize):
            parentA = self.individuals[j % len(self.individuals)]
            parentBIndex = j
            while parentBIndex == j:
                parentBIndex = random.sample(list(range(len(self.individuals))), 1)[0]
            parentB = self.individuals[parentBIndex]
            baby = parentA.makeBabyWith(parentB)
            baby.nSwap(Config.amountBitSwaps)
            offspring.append(baby)
        return offspring

    def updateFrequencyTable(self, individual):
        objectiveValue = individual.getObjectiveValue()
        self.frequency[objectiveValue] += 1

    def selectBest(self, offspring, amount):
        selectionPool = self.individuals + offspring
        selectionPool.sort()
        return selectionPool[:amount]

    def selectBestPreferOffspring(self, offspring):
        if offspring[0].getObjectiveValue() <= self.individuals[0].getObjectiveValue():
            return offspring
        return self.individuals

    def selectLeastFrequent(self, offspring, amount):
        selectionPool = self.individuals + offspring

        for individual in selectionPool:
            self.updateFrequencyTable(individual)

        frequencyTable = {
            'individual': [],
            'objectiveValue': [],
            'frequency': []
        }

        for individual in selectionPool:
            objectiveValue = individual.getObjectiveValue()
            frequency = self.frequency[objectiveValue]

            frequencyTable['individual'].append(individual)
            frequencyTable['objectiveValue'].append(objectiveValue)
            frequencyTable['frequency'].append(frequency)

        dataFrame = pd.DataFrame.from_dict(frequencyTable)
        sortedDataFrame = dataFrame.sort_values(by=['frequency', 'objectiveValue'])

        return sortedDataFrame['individual'].tolist()[:amount]

    def selectLeastFrequentPreferOffspring(self, offspring):
        selectionPool = self.individuals + offspring

        for individual in selectionPool:
            self.updateFrequencyTable(individual)

        if self.frequency[offspring[0].getObjectiveValue()] <= self.frequency[self.individuals[0].getObjectiveValue()]:
            return offspring
        return self.individuals

    def fromIndividualSequenceList(self, sequenceList, instance):
        self.individuals = []
        for sequence in sequenceList:
            self.individuals.append(SimpleEncoding(sequence, instance))

    def getMinimumAndMaximumObjectiveValue(self):
        minimum = math.inf
        maximum = 0
        for individual in self.individuals:
            if individual.getObjectiveValue() > maximum:
                maximum = individual.getObjectiveValue()
            if individual.getObjectiveValue() < minimum:
                minimum = individual.getObjectiveValue()

        return minimum, maximum

    def getMinimumAndMaximumFFAValue(self):
        return min(self.frequency.values()), max(self.frequency.values())

    def getIndividualsString(self):
        result = ''
        for individual in self.individuals:
            result += ';' + str(individual.sequence)
        return result[1:]

    def getObjectiveValuesList(self):
        result = []
        for individual in self.individuals:
            result.append(individual.getObjectiveValue())
        return result
