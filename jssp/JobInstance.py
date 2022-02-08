class JobInstance:
    def __init__(self, machineId, executionTime):
        self.machineId = machineId
        self.executionTime = executionTime

    def __repr__(self):
        return "{} => {}".format(self.machineId, self.executionTime)