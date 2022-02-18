import itertools
import random
from abc import ABC
from collections import defaultdict

from Config import Config
from genotype.Genotype import Genotype
from phenotype.MachineJob import MachineJob
from phenotype.Phenotype import Phenotype


class SimpleEncoding(Genotype, ABC):

    def __init__(self, sequence):
        self.sequence = sequence
        self.objectiveValue = 0
        self.isBestOfNeighbourhood = False

    def __lt__(self, otherSimpleEncoding):
        return self.getObjectiveValue() < otherSimpleEncoding.getObjectiveValue()

    def toPhenotype(self):
        resultMachineList = defaultdict(lambda: [], {})
        amountMachinesFinished = defaultdict(lambda: 0, {})
        endTimeMachine = defaultdict(lambda: 0, {})
        endTimeJob = defaultdict(lambda: 0, {})

        for jobId in self.sequence:
            currentJob = Config.jssp.jobList[jobId][amountMachinesFinished[jobId]]
            jobTime = currentJob.executionTime
            machineId = currentJob.machineId

            currentStartTime = max(endTimeMachine[machineId], endTimeJob[jobId])
            currentEndTime = currentStartTime + jobTime

            machineJob = MachineJob(jobId, currentStartTime, currentEndTime)
            resultMachineList[machineId].append(machineJob)

            endTimeMachine[machineId] = currentEndTime
            endTimeJob[jobId] = currentEndTime
            amountMachinesFinished[jobId] += 1

        return Phenotype(resultMachineList)

    def nSwap(self, n):
        if self.isBestOfNeighbourhood:
            return

        for i in range(n):
            self.isBestOfNeighbourhood = True

            swaps = list(itertools.permutations(range(len(self.sequence)), 2))
            random.shuffle(swaps)

            for (firstIndex, secondIndex) in swaps:
                newSimpleEncoding = self.singleSwap(firstIndex, secondIndex)
                if newSimpleEncoding.__lt__(self):
                    self.sequence = newSimpleEncoding.sequence
                    self.objectiveValue = newSimpleEncoding.getObjectiveValue()
                    self.isBestOfNeighbourhood = False
                    break

    def singleSwap(self, firstIndex, secondIndex):
        newSequence = self.sequence.copy()
        newSequence[firstIndex], newSequence[secondIndex] = newSequence[secondIndex], newSequence[firstIndex]
        newSimpleEncoding = SimpleEncoding(newSequence)
        return newSimpleEncoding

    def randomSingleSwap(self):
        firstIndex = random.randint(0, len(self.sequence) - 1)
        secondIndex = firstIndex
        while secondIndex == firstIndex:
            secondIndex = random.randint(0, len(self.sequence) - 1)
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

        baby = SimpleEncoding(babySequence)
        return baby

    def getObjectiveValue(self):
        #if self.objectiveValue == 0:
        #    self.objectiveValue = self.toPhenotype().getObjectiveValue()
        return self.objectiveValue
