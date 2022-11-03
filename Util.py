import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import numpy as np
import os
import gc

from os.path import exists
from scipy.stats import norm
import matplotlib.mlab as mlab
from jssp.JSSPFactory import JSSPFactory


class Util:

    @staticmethod
    def createAllResultsFile():
        allDict = {
            'instance': [],
            'run': [],
            'jobs': [],
            'machines': [],
            'hc': [],
            'ffa': [],
            'bks': [],
        }
        library = Util.readFullLibrary('files/jssp-instances/full_full_library.txt')
        bestKnown = Util.readFullLibraryBestKnown('files/jssp-instances/full_full_library.txt')
        for run in os.listdir(resultFolder):
            for subFolder in os.listdir(resultFolder + run):
                jssp = JSSPFactory.generateJSSPFromFormat(library[subFolder])
                hcFile = open(resultFolder + run + "/" + subFolder + "/hc.txt")
                ffaFile = open(resultFolder + run + "/" + subFolder + "/fhc.txt")
                hcResult = int(hcFile.read())
                ffaResult = int(ffaFile.read())
                allDict['instance'].append(subFolder)
                allDict['run'].append(run)
                allDict['jobs'].append(jssp.amountJobs)
                allDict['machines'].append(jssp.amountMachines)
                allDict['hc'].append(hcResult)
                allDict['ffa'].append(ffaResult)
                allDict['bks'].append(bestKnown[subFolder])

        df = pd.DataFrame(allDict)
        df.to_csv('allResults.csv', index=False)

    @staticmethod
    def createFunctionEvaluationsPlot():
        populationsFolder = 'files/output/hc2/populations/'
        library = Util.readFullLibrary('files/jssp-instances/full_full_library.txt')
        bestKnown = Util.readFullLibraryBestKnown('files/jssp-instances/full_full_library.txt')
        for run in os.listdir(populationsFolder):
            for subFolder in os.listdir(populationsFolder + run):
                if (exists('files/output/hc2/results/' + run + "/" + subFolder + "/plot.png")):
                    print(subFolder + " exists!")
                    continue
                jssp = JSSPFactory.generateJSSPFromFormat(library[subFolder])
                fileName = populationsFolder + run + "/" + subFolder + "/"
                fileHC = open(fileName + 'hc.txt')
                fileFHC = open(fileName + 'fhc.txt')

                recordsHc = fileHC.readline().split(', ')[:-1]
                xHc = []
                yHc = []
                for record in recordsHc:
                    xHc.append(int(record.split(':')[0]))
                    yHc.append(int(record.split(':')[1]))

                recordsFfa = fileFHC.readline().split(', ')[:-1]
                xFfa = []
                yFfa = []
                for record in recordsFfa:
                    xFfa.append(int(record.split(':')[0]))
                    yFfa.append(int(record.split(':')[1]))

                xBks = [0, pow(2, 30)]
                yBks = [bestKnown[subFolder], bestKnown[subFolder]]

                plt.plot(xHc, yHc, label='Hill Climber', c='orange')
                plt.plot(xFfa, yFfa, label='FFA', c='blue')
                plt.plot(xBks, yBks, label='Best known solution', c='black')
                plt.xscale('log')
                plt.legend()
                plt.xlabel('Function Evaluations')
                plt.ylabel('Objective Value (Makespan)')
                plt.title(subFolder + "(" + str(jssp.amountMachines) + " machines and " + str(jssp.amountJobs) + " jobs)")
                plt.savefig('files/output/hc2/results/' + run + '/' + subFolder + '/plot.png')
                plt.figure().clear()
                plt.close('all')
                print(subFolder + " done!")

    @staticmethod
    def createFunctionEvaluationsPlotPpa(resultFolder, library, instanceName):
        jssp = JSSPFactory.generateJSSPFromFormat(library[instanceName])
        fileName = resultFolder + instanceName + "/"
        filePpa = open(fileName + 'ppaAllBest.txt')
        fileFfaSelect = open(fileName + 'ffaSelectAllBest.txt')
        fileFfaComplete = open(fileName + 'ffaCompleteAllBest.txt')

        recordsPpa = filePpa.readline().split(', ')[:-1]
        xPpa = []
        yPpa = []
        for record in recordsPpa:
            xPpa.append(int(record.split(':')[0]))
            yPpa.append(int(record.split(':')[1]))

        recordsFfaSelect = fileFfaSelect.readline().split(', ')[:-1]
        xFfaSelect = []
        yFfaSelect = []
        for record in recordsFfaSelect:
            xFfaSelect.append(int(record.split(':')[0]))
            yFfaSelect.append(int(record.split(':')[1]))

        recordsFfaComplete = fileFfaComplete.readline().split(', ')[:-1]
        xFfaComplete = []
        yFfaComplete = []
        for record in recordsFfaComplete:
            xFfaComplete.append(int(record.split(':')[0]))
            yFfaComplete.append(int(record.split(':')[1]))

        plt.plot(xPpa, yPpa, label='PPA')
        plt.plot(xFfaSelect, yFfaSelect, label='FFA Select')
        plt.plot(xFfaComplete, yFfaComplete, label='FFA Complete')
        plt.xscale('log')
        plt.legend()
        plt.xlabel('Function Evaluations')
        plt.ylabel('Objective Value (Execution time)')
        plt.title(instanceName + "(" + str(jssp.amountMachines) + " machines and " + str(jssp.amountJobs) + " jobs)")
        plt.show()

    @staticmethod
    def plotBoth(library, instanceNames):
        yPPAs = []
        yFFAs = []
        yFFACompletes = []
        xPPAs = []
        xFFAs = []
        xFFACompletes = []
        intermediateHCs = []
        intermediateFHCs = []
        xAxises = []
        titles = []
        for instanceName in instanceNames:
            resultFolderPPA = 'files/output/ppa/populations/1/'
            resultFolderHC = 'files/output/hc/populations/1/'
            jssp = JSSPFactory.generateJSSPFromFormat(library[instanceName])
            fileName = resultFolderPPA + instanceName + "/"
            filePpa = open(fileName + 'ppaAllBest.txt')
            fileFfaSelect = open(fileName + 'ffaSelectAllBest.txt')
            fileFfaComplete = open(fileName + 'ffaCompleteAllBest.txt')
            fileName = resultFolderHC + instanceName + "/"
            fileHC = open(fileName + 'hc.txt')
            fileFHC = open(fileName + 'fhc.txt')

            recordsPpa = filePpa.readline().split(', ')[:-1]
            xPpa = []
            yPpa = []
            for record in recordsPpa:
                xPpa.append(int(record.split(':')[0]))
                yPpa.append(int(record.split(':')[1]))

            recordsFfaSelect = fileFfaSelect.readline().split(', ')[:-1]
            xFfaSelect = []
            yFfaSelect = []
            for record in recordsFfaSelect:
                xFfaSelect.append(int(record.split(':')[0]))
                yFfaSelect.append(int(record.split(':')[1]))

            recordsFfaComplete = fileFfaComplete.readline().split(', ')[:-1]
            xFfaComplete = []
            yFfaComplete = []
            for record in recordsFfaComplete:
                xFfaComplete.append(int(record.split(':')[0]))
                yFfaComplete.append(int(record.split(':')[1]))

            yPPAs.append(yPpa)
            yFFAs.append(yFfaSelect)
            yFFACompletes.append(yFfaComplete)
            xPPAs.append(xPpa)
            xFFAs.append(xFfaSelect)
            xFFACompletes.append(xFfaComplete)

            intermediateResultsHC = list(map(int, fileHC.readline().split(', ')[:-2]))
            intermediateResultsFHC = list(map(int, fileFHC.readline().split(', ')[:-1]))
            intermediateResultsHC.insert(0, None)

            xAxis = []
            for i in range(len(intermediateResultsFHC)):
                xAxis.append((i * 1000) + 1)
            intermediateHCs.append(intermediateResultsHC)
            intermediateFHCs.append(intermediateResultsFHC)
            xAxises.append(xAxis)
            titles.append(instanceName + "(" + str(jssp.amountMachines) + " machines and " + str(jssp.amountJobs) + " jobs)")

        fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True)
        ax1.plot(xPPAs[0], yPPAs[0], label='PPA Standard')
        ax1.plot(xFFAs[0], yFFAs[0], label='PPA FFA Select')
        ax1.plot(xFFACompletes[0], yFFACompletes[0], label='PPA FFA Complete')
        ax1.plot(xAxises[0], intermediateHCs[0], label='HC')
        ax1.plot(xAxises[0], intermediateFHCs[0], label='HC FFA')
        ax1.set_title(titles[0])
        ax2.plot(xPPAs[1], yPPAs[1])
        ax2.plot(xFFAs[1], yFFAs[1])
        ax2.plot(xFFACompletes[1], yFFACompletes[1])
        ax2.plot(xAxises[1], intermediateHCs[1])
        ax2.plot(xAxises[1], intermediateFHCs[1])
        ax2.set_title(titles[1])
        plt.xscale('log')
        fig.text(0.5, 0.04, 'Function Evaluations', ha='center', fontsize=16)
        fig.text(0.04, 0.5, 'Objective Value (Execution time)', va='center', rotation='vertical', fontsize=16)
        handles, labels = ax1.get_legend_handles_labels()
        fig.legend(handles, labels, loc=7)

        plt.show()

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
        n, bins, patches = plt.hist(x=executionTimes, color='#0504aa',
                                    alpha=0.7, rwidth=0.9, bins=30)
        (average, stdv) = np.round(norm.fit(executionTimes), 2)
        y = norm.pdf(bins, average, stdv)
        l = plt.plot(bins, y * 0.03333 * sum(executionTimes), 'r--', linewidth=2)
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Objective Value')
        plt.ylabel('Number of Solutions')
        plt.title("Objective value distribution for instance ft06\n6 jobs and 6 machines, " + r'$\mu$=' + str(average)
                  + " and " + r'$\sigma$=' + str(stdv))
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

# from jssp.JSSPFactory import JSSPFactory
#
# library = Util.readFullLibrary('files/jssp-instances/full_full_library.txt')
#
# subFolders = ['dmu80', 'orb03', 'dmu79', 'swv05', 'dmu76', 'dmu50']
# resultFolder = 'files/output/hc/populations/1/'
# intermediateHCs = []
# intermediateFHCs = []
# xAxises = []
# titles = []
# for subFolder in subFolders:
#     jssp = JSSPFactory.generateJSSPFromFormat(library[subFolder])
#     fileName = resultFolder + subFolder + "/"
#     fileHC = open(fileName + 'hc.txt')
#     fileFHC = open(fileName + 'fhc.txt')
#
#     intermediateResultsHC = list(map(int, fileHC.readline().split(', ')[:-2]))
#     intermediateResultsFHC = list(map(int, fileFHC.readline().split(', ')[:-1]))
#     intermediateResultsHC.insert(0, None)
#
#     xAxis = []
#     for i in range(len(intermediateResultsHC)):
#         xAxis.append((i * 1000) + 1)
#
#     intermediateHCs.append(intermediateResultsHC)
#     intermediateFHCs.append(intermediateResultsFHC)
#     xAxises.append(xAxis)
#     titles.append(subFolder + "(" + str(jssp.amountMachines) + " machines and " + str(jssp.amountJobs) + " jobs)")
#
# fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, sharex=True)
# ax1.plot(xAxises[0], intermediateHCs[0], label='Hill Climber')
# ax1.plot(xAxises[0], intermediateFHCs[0], label='FFA')
# ax1.set_title(titles[0])
# ax2.plot(xAxises[1], intermediateHCs[1])
# ax2.plot(xAxises[1], intermediateFHCs[1])
# ax2.set_title(titles[1])
# ax3.plot(xAxises[2], intermediateHCs[2])
# ax3.plot(xAxises[2], intermediateFHCs[2])
# ax3.set_title(titles[2])
# ax4.plot(xAxises[3], intermediateHCs[3])
# ax4.plot(xAxises[3], intermediateFHCs[3])
# ax4.set_title(titles[3])
# ax5.plot(xAxises[4], intermediateHCs[4])
# ax5.plot(xAxises[4], intermediateFHCs[4])
# ax5.set_title(titles[4])
# ax6.plot(xAxises[5], intermediateHCs[5])
# ax6.plot(xAxises[5], intermediateFHCs[5])
# ax6.set_title(titles[5])
# plt.xscale('log')
# fig.text(0.5, 0.04, 'Function Evaluations', ha='center', fontsize=16)
# fig.text(0.04, 0.5, 'Objective Value (Execution time)', va='center', rotation='vertical', fontsize=16)
# handles, labels = ax1.get_legend_handles_labels()
# fig.legend(handles, labels, loc=9)
#
# plt.show()

# plt.plot(xAxis, intermediateResultsHC, label='Hill Climber')
# plt.plot(xAxis, intermediateResultsFHC, label='FFA')
# plt.xscale('log')
# plt.show()

# plt.legend()
# plt.xlabel('Function Evaluations')
# plt.ylabel('Objective Value (Execution time)')
# plt.title(subFolder + "(" + str(jssp.amountMachines) + " machines and " + str(jssp.amountJobs) + " jobs)")