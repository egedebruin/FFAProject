import itertools
import math
import random
from abc import ABC
from collections import defaultdict

from Config import Config
from genotype.Genotype import Genotype
from phenotype.Phenotype import Phenotype


class SimpleEncoding(Genotype, ABC):

    def __init__(self, sequence, instance=None):
        self.sequence = sequence
        self.objectiveValue = 0
        self.isBestOfNeighbourhood = False

        self.jsspInstance = Config.jssp
        if instance is not None:
            self.jsspInstance = instance

    def __lt__(self, otherSimpleEncoding):
        return self.getObjectiveValue() < otherSimpleEncoding.getObjectiveValue()

    def toPhenotype(self):
        resultMachineList = defaultdict(lambda: [], {})
        amountMachinesFinished = defaultdict(lambda: 0, {})
        endTimeMachine = defaultdict(lambda: 0, {})
        endTimeJob = defaultdict(lambda: 0, {})

        highestEndTime = 0
        for jobId in self.sequence:
            currentJob = self.jsspInstance.jobList[jobId][amountMachinesFinished[jobId]]
            jobTime = currentJob.executionTime
            machineId = currentJob.machineId

            currentStartTime = endTimeMachine[machineId]
            if endTimeJob[jobId] > currentStartTime:
                currentStartTime = endTimeJob[jobId]
            currentEndTime = currentStartTime + jobTime

            if currentEndTime > highestEndTime:
                highestEndTime = currentEndTime

            machineJob = {
                'jobId': jobId,
                'startTime': currentStartTime,
                'endTime': currentEndTime
            }
            resultMachineList[machineId].append(machineJob)

            endTimeMachine[machineId] = currentEndTime
            endTimeJob[jobId] = currentEndTime
            amountMachinesFinished[jobId] += 1

        return Phenotype(resultMachineList, highestEndTime)

    def nSwap(self, n):
        for i in range(n):
            if self.isBestOfNeighbourhood:
                return
            self.isBestOfNeighbourhood = True

            swaps = list(itertools.permutations(range(len(self.sequence)), 2))
            random.shuffle(swaps)

            for (firstIndex, secondIndex) in swaps:
                if self.sequence[firstIndex] == self.sequence[secondIndex]:
                    continue
                newSimpleEncoding = self.singleSwap(firstIndex, secondIndex)
                if newSimpleEncoding.__lt__(self):
                    self.sequence = newSimpleEncoding.sequence
                    self.objectiveValue = newSimpleEncoding.getObjectiveValue()
                    self.isBestOfNeighbourhood = False
                    break

    def singleSwap(self, firstIndex, secondIndex):
        newSequence = self.sequence.copy()
        newSequence[firstIndex], newSequence[secondIndex] = newSequence[secondIndex], newSequence[firstIndex]
        newSimpleEncoding = SimpleEncoding(newSequence, self.jsspInstance)
        return newSimpleEncoding

    def singleSwapInPlace(self, firstIndex, secondIndex):
        self.sequence[firstIndex], self.sequence[secondIndex] = self.sequence[secondIndex], self.sequence[firstIndex]

    def randomSingleSwap(self, inPlace=False):
        firstIndex = random.randint(0, len(self.sequence) - 1)
        secondIndex = firstIndex
        while secondIndex == firstIndex:
            secondIndex = random.randint(0, len(self.sequence) - 1)

        if inPlace:
            return self.singleSwapInPlace(firstIndex, secondIndex)
        return self.singleSwap(firstIndex, secondIndex)

    def makeBabyWith(self, otherSimpleEncoding):
        babySequence = []
        parentASequence = self.sequence.copy()
        parentBSequence = otherSimpleEncoding.sequence.copy()

        for i in range(len(self.sequence)):
            newValue = parentASequence[0]
            if random.uniform(0, 1) > 0.5:
                newValue = parentBSequence[0]

            parentASequence.remove(newValue)
            parentBSequence.remove(newValue)
            babySequence.append(newValue)

        baby = SimpleEncoding(babySequence, self.jsspInstance)
        return baby

    def getObjectiveValue(self):
        if self.objectiveValue == 0:
            self.objectiveValue = self.toPhenotype().getObjectiveValue()
        return self.objectiveValue

    def getPpaFitnessValue(self, minimum, maximum, value):
        if minimum == maximum:
            return 0.5

        normalised = float((maximum - value) / (maximum - minimum))

        ppaFitness = 0.5 * (math.tanh(4 * normalised - 2) + 1)
        return ppaFitness
