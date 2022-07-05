from collections import defaultdict
import os
import json

from Config import Config


class RestartConfig:

    def __init__(self):
        self.functionEvaluations = 1
        self.currentPopulation = None
        self.currentBest = 0
        self.frequencyTable = None

    def setRestartValuesNormalHillClimber(self, instanceName, run):
        fileName = '/current_hc.txt'
        if os.path.exists(Config.intermediateFolder + str(run) + "/" + instanceName + fileName):
            file = open(Config.intermediateFolder + str(run) + "/" + instanceName + fileName)
            line = file.readline().split(',', 1)

            self.functionEvaluations = int(line[0])
            self.currentPopulation = list(map(int, line[1].replace('[', '').replace(']', '').split(',')))

    def setRestartValuesFFAHillClimber(self, instanceName, run):
        currentFileName = '/current_fhc.txt'
        allFileName = '/fhc.txt'
        if os.path.exists(Config.intermediateFolder + str(run) + "/" + instanceName + allFileName):
            file = open(Config.intermediateFolder + str(run) + "/" + instanceName + allFileName)
            self.currentBest = file.read().split(',')[-2]
        if os.path.exists(Config.intermediateFolder + str(run) + "/" + instanceName + currentFileName):
            file = open(Config.intermediateFolder + str(run) + "/" + instanceName + currentFileName)
            line = file.readline().split(',', 1)
            secondLine = file.readline()

            self.frequencyTable = defaultdict(lambda: 0, json.loads(secondLine))
            self.functionEvaluations = int(line[0])
            self.currentPopulation = list(map(int, line[1].replace('[', '').replace(']', '').split(',')))

    #TODO: Get restart values for PPA