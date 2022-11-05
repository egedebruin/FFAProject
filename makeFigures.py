import matplotlib.pyplot as plt
from jssp.JSSPFactory import JSSPFactory
from Util import Util
import os
from os.path import exists

populationsFolder = 'files/output/hc2/populations/'
instances = ['dmu80', 'dmu79', 'dmu76', 'orb03', 'orb08', 'orb10']
library = Util.readFullLibrary('files/jssp-instances/full_full_library.txt')
bestKnown = Util.readFullLibraryBestKnown('files/jssp-instances/full_full_library.txt')
fig, ax = plt.subplots(3, 2, sharex='all')
i = 0
j = 0
for instance in instances:
    jssp = JSSPFactory.generateJSSPFromFormat(library[instance])
    for run in os.listdir(populationsFolder):
        fileName = populationsFolder + run + "/" + instance + "/"
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
        yBks = [bestKnown[instance], bestKnown[instance]]

        if run == '1':
            ax[i][j].plot(xHc, yHc, c='orange', alpha=0.5, label='HC')
            ax[i][j].plot(xFfa, yFfa, c='blue', alpha=0.5, label='FFA')
            ax[i][j].plot(xBks, yBks, c='black', alpha=0.1, linestyle='dashed', label='Best known solution')
        else:
            ax[i][j].plot(xHc, yHc, c='orange', alpha=0.5)
            ax[i][j].plot(xFfa, yFfa, c='blue', alpha=0.5)
            ax[i][j].plot(xBks, yBks, c='black', alpha=0.1, linestyle='dashed')
    if j == 1:
        ax[i][j].yaxis.tick_right()
    if i == 0 and j == 1:
        ax[i][j].legend(loc='right', fontsize=12)
    if i < 2:
        ax[i][j].tick_params(bottom=False)

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax[i][j].text(0.75, 0.75, instance + "\n" + 'jobs: ' + str(jssp.amountJobs) + "\n" + 'machines: '
                  + str(jssp.amountMachines), transform=ax[i][j].transAxes, bbox=props, fontsize=12)

    i += 1
    if i == 3:
        i = 0
        j += 1
plt.xscale('log')
fig.text(0.5, 0.04, 'Function Evaluations', ha='center', fontsize=16)
fig.text(0.04, 0.5, 'Objective Value (Makespan)', va='center', rotation='vertical', fontsize=16)
plt.subplots_adjust(wspace=0, hspace=0)
plt.show()
