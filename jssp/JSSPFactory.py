import io
import random

from jssp.JSSPInstance import JSSPInstance
from jssp.JobInstance import JobInstance


class JSSPFactory:

    @staticmethod
    def generateJSSPFromFormat(jsspFormat):
        file = io.StringIO(jsspFormat)
        jobList = {}

        firstLine = file.readline()
        jobs = int(firstLine.split()[0])
        machines = int(firstLine.split()[1])

        for i in range(jobs):
            jobValues = {}
            lineValues = file.readline().split()
            for j in range(machines):
                machineId = int(lineValues[j * 2])
                machineTime = int(lineValues[(j * 2) + 1])
                job = JobInstance(machineId, machineTime)
                jobValues[j] = job
            jobList[i] = jobValues

        return JSSPInstance(jobs, machines, jobList)

    @staticmethod
    def generateJSSPRandom(jobs, machines, randomizer='none'):
        jobList = {}
        for i in range(jobs):
            jobValues = {}
            machineIds = list(range(0, machines))
            random.shuffle(machineIds)
            for j in range(machines):
                machineId = machineIds[j]
                machineTime = JSSPFactory.getRandomNumber(randomizer)
                job = JobInstance(machineId, machineTime)
                jobValues[j] = job
            jobList[i] = jobValues
        return JSSPInstance(jobs, machines, jobList)

    @staticmethod
    def getRandomNumber(randomizer):
        if randomizer == 'none':
            return 5
        if randomizer == 'uniform':
            return int(random.uniform(1, 10))
        if randomizer == 'exponential':
            return int(random.expovariate(1))
        if randomizer == 'gaussian':
            return int(random.gauss(5, 2))
        else:
            raise ValueError("Oh no, incorrect randomizer used.")