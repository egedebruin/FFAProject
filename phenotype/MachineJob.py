class MachineJob:
    def __init__(self, jobId, startTime, endTime):
        self.jobId = jobId
        self.startTime = startTime
        self.endTime = endTime

    def __repr__(self):
        return "[{}: {} => {}]".format(self.jobId, self.startTime, self.endTime)