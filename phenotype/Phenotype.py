from collections import defaultdict
import pandas as pd


class Phenotype:

    def __init__(self, machineList, objectiveValue):
        self.machineList = machineList
        self.objectiveValue = objectiveValue

    def getObjectiveValue(self):
        return self.objectiveValue

    def toDataFrame(self):
        result = defaultdict(lambda: [], {})
        for machineId, jobs in self.machineList.items():
            for job in jobs:
                result['machineId'].append(machineId)
                result['jobId'].append(job['jobId'])
                result['executionTime'].append(job['endTime'] - job['startTime'])
                result['startTime'].append(job['startTime'])

        dataFrame = pd.DataFrame.from_dict(result)
        return dataFrame
