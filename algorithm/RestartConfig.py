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
        self.reset = False

    def setRestartValuesNormalHillClimber(self, instanceName, run):
        fileName = '/current_hc.txt'
        if os.path.exists(Config.intermediateFolder + str(run) + "/" + instanceName + fileName):
            file = open(Config.intermediateFolder + str(run) + "/" + instanceName + fileName)
            line = file.readline().split(',', 1)

            self.functionEvaluations = int(line[0])
            self.currentPopulation = list(map(int, line[1].replace('[', '').replace(']', '').split(',')))

    def setRestartValuesFFAHillClimber(self, instanceName, run):
        currentFileName = '/current_fhc.txt'
        if os.path.exists(Config.intermediateFolder + str(run) + "/" + instanceName + currentFileName):
            file = open(Config.intermediateFolder + str(run) + "/" + instanceName + currentFileName)
            line = file.readline().split(',', 1)
            secondLine = file.readline()
            thirdLine = file.readline()

            self.frequencyTable = defaultdict(lambda: 0, json.loads(secondLine))
            self.functionEvaluations = int(line[0])
            self.currentPopulation = list(map(int, line[1].replace('[', '').replace(']', '').split(',')))
            self.currentBest = list(map(int, thirdLine.replace('[', '').replace(']', '').split(',')))

    def setRestartValuesPpa(self, instanceName, run, currentFileName):
        if os.path.exists(Config.intermediateFolder + str(run) + "/" + instanceName + currentFileName):
            self.reset = True
            file = open(Config.intermediateFolder + str(run) + "/" + instanceName + currentFileName)
            line = file.readline().split(',', 1)
            secondLine = file.readline()
            thirdLine = file.readline()

            population = []
            for individual in line[1].split(';'):
                population.append(list(map(int, individual.replace('[', '').replace(']', '').split(','))))

            self.functionEvaluations = int(line[0])
            self.currentPopulation = population

            if secondLine != 'null\n':
                self.frequencyTable = defaultdict(lambda: 0, json.loads(secondLine))
            if thirdLine != 'None':
                self.currentBest = list(map(int, thirdLine.replace('[', '').replace(']', '').split(',')))
