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
            improved = False
            swapsTried = 0

            while not improved:
                newSimpleEncoding = self.singleSwap()
                if newSimpleEncoding.__lt__(self):
                    improved = True
                    self.sequence = newSimpleEncoding.sequence
                swapsTried += 1

                if swapsTried >= (Config.jssp.amountJobs * Config.jssp.amountMachines):
                    self.isBestOfNeighbourhood = True
                    return

    def singleSwap(self):
        newSequence = self.sequence.copy()
        first, second = random.sample(range(len(newSequence)), 2)
        newSequence[first], newSequence[second] = newSequence[second], newSequence[first]
        newSimpleEncoding = SimpleEncoding(newSequence)
        return newSimpleEncoding

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
        if self.objectiveValue == 0:
            self.objectiveValue = self.toPhenotype().getObjectiveValue()
        return self.objectiveValue
