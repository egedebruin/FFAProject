import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import numpy as np
import os
import gc

from jssp.JSSPFactory import JSSPFactory


class Util:

    @staticmethod
    def createAllResultsFile(library):
        bestKnown = Util.readFullLibraryBestKnown(library)
        resultFolder = 'files/output/hc/results/1/'
        allDict = {'instance': [],
                   'jobs': [],
                   'machines': [],
                   'hill climber': [],
                   'ffa': [],
                   'best known solution': []}
        for subFolder in os.listdir(resultFolder):
            jssp = JSSPFactory.generateJSSPFromFormat(library[subFolder])
            if not os.path.exists(resultFolder + subFolder + "/fhc.txt"):
                continue
            hcFile = open(resultFolder + subFolder + "/hc.txt")
            ffaFile = open(resultFolder + subFolder + "/fhc.txt")
            hcResult = int(hcFile.read())
            ffaResult = int(ffaFile.read())

            allDict['instance'].append(subFolder)
            allDict['jobs'].append(jssp.amountJobs)
            allDict['machines'].append(jssp.amountMachines)
            allDict['hill climber'].append(hcResult)
            allDict['ffa'].append(ffaResult)
            allDict['best known solution'].append(bestKnown[subFolder])

        df = pd.DataFrame(allDict)
        df.to_csv('allResults.csv', index=False)

    @staticmethod
    def createFunctionEvaluationsPlot(resultFolder, library):
        ole = False
        for subFolder in os.listdir(resultFolder):
            if ole or subFolder == 'yn1':
                ole = True
            else:
                continue
            jssp = JSSPFactory.generateJSSPFromFormat(library[subFolder])
            fileName = resultFolder + subFolder + "/"
            fileHC = open(fileName + 'hc.txt')
            fileFHC = open(fileName + 'fhc.txt')

            intermediateResultsHC = list(map(int, fileHC.readline().split(', ')[:-2]))
            intermediateResultsFHC = list(map(int, fileFHC.readline().split(', ')[:-1]))
            intermediateResultsHC.insert(0, None)

            xAxis = []
            for i in range(len(intermediateResultsHC)):
                xAxis.append((i * 1000) + 1)

            plt.plot(xAxis, intermediateResultsHC, label='Hill Climber')
            plt.plot(xAxis, intermediateResultsFHC, label='FFA')
            plt.xscale('log')
            plt.legend()
            plt.xlabel('Function Evaluations')
            plt.ylabel('Objective Value (Execution time)')
            plt.title(subFolder + "(" + str(jssp.amountMachines) + " machines and " + str(jssp.amountJobs) + " jobs)")
            plt.savefig('files/output/hc/results/1/' + subFolder + '/plot.png')
            plt.figure().clear()
            plt.close('all')
            plt.cla()
            plt.clf()
            gc.collect()

            print(subFolder + " done!")

    @staticmethod
    def resultsToLatex(resultsFileName):
        df = pd.read_csv(resultsFileName)
        df['hc'] = df['hc'].astype('string')
        df['bks'] = df['bks'].astype('string')
        df['ffa'] = df['ffa'].astype('string')
        df['hc'] = np.where(df['hc'] == df['bks'], '\\textbf{' + df['hc'] + "}", df['hc'])
        df['ffa'] = np.where(df['ffa'] == df['bks'], '\\textbf{' + df['ffa'] + "}", df['ffa'])
        print(df.to_latex(index=False, longtable=False, escape=False,
                          caption='Caption this is a table be happy with it please.'))

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
        plt.hist(executionTimes, bins=30)
        plt.legend()
        plt.xlabel('Objective Value')
        plt.ylabel('Amount of solutions')
        plt.title("Random instance with 10 machines and 10 jobs")
        plt.savefig('Distribution_graph3')
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
        bks = {}

        for line in file:
            line = line[1:]
            if instanceName == '' and 'instance' in line:
                instanceName = line.replace('instance', '').replace('\n', '').replace(' ', '')
                continue
            if ('instance' in line) or ('best known solution' in line):
                copyLines = True
                bestKnown = int(line.split('best known solution: ')[1])
                bks[instanceName] = bestKnown
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

    @staticmethod
    def readFullLibraryBestKnown(fileName):
        file = open(fileName)
        instanceName = ''
        copyLines = False
        bks = {}

        for line in file:
            line = line[1:]
            if instanceName == '' and 'instance' in line:
                instanceName = line.replace('instance', '').replace('\n', '').replace(' ', '')
                continue
            if 'best known solution' in line:
                copyLines = True
                bestKnown = int(line.split('best known solution: ')[1])
                bks[instanceName] = bestKnown
                continue
            if '+++' in line and copyLines is True:
                copyLines = False
                instanceName = ''
                continue

        return bks
