import matplotlib.pyplot as plt
import matplotlib.cm as cm


class Util:

    @staticmethod
    def showGanttChart(instance, amountJobs):
        dataFrame = instance.toDataFrame()
        sortedDataframe = dataFrame.sort_values(by=['machineId', 'jobId'])
        fig, ax = plt.subplots(1, figsize=(16, 6))
        chart = ax.barh(sortedDataframe.machineId, sortedDataframe.executionTime, left=sortedDataframe.startTime,
                        color=cm.hot(sortedDataframe.jobId / amountJobs))
        plt.legend(chart, ["Job " + str(number) for number in list(sortedDataframe.jobId)[:amountJobs]])
        plt.show()

    @staticmethod
    def showTimeHistogram(executionTimes):
        plt.hist(executionTimes, bins=50)
        plt.show()

    @staticmethod
    def readSimpleFile(fileName):
        file = open(fileName)

        text = file.read()

        return {"demo": text}

    @staticmethod
    def readFullLibrary(fileName):
        file = open(fileName)
        result = {}
        instanceName = ''
        instance = ''
        copyLines = False

        for line in file:
            line = line[1:]
            if instanceName == '' and 'instance' in line:
                instanceName = line.replace('instance', '').replace('\n', '').replace(' ', '')
                continue
            if 'instance' in line:
                copyLines = True
                continue
            if '+++' in line and copyLines is True:
                result[instanceName] = instance
                copyLines = False
                instanceName = ''
                instance = ''
                continue
            if copyLines:
                instance += line

        return result
