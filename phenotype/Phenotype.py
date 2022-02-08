from collections import defaultdict
import pandas as pd

class Phenotype:

    def __init__(self, machineList):
        self.machineList = machineList

    def getObjectiveValue(self):
        result = 0
        for machineId, jobs in self.machineList.items():
            for machineJob in jobs:
                if machineJob.endTime > result:
                    result = machineJob.endTime

        return result

    def toDataFrame(self):
        result = defaultdict(lambda: [], {})
        for machineId, jobs in self.machineList.items():
            for job in jobs:
                result['machineId'].append(machineId)
                result['jobId'].append(job.jobId)
                result['executionTime'].append(job.endTime - job.startTime)
                result['startTime'].append(job.startTime)

        dataFrame = pd.DataFrame.from_dict(result)
        return dataFrame
