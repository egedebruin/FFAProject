import os

from Config import Config
from genotype.GenotypeFactory import GenotypeFactory
import time
import json

from genotype.SimpleEncoding import SimpleEncoding


class Algorithm:

    @staticmethod
    def memeticAlgorithm():
        allPopulations = []
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(Config.populationSize)
        best = population.selectBest([], 1)[0]
        allPopulations.append(population.getIndividualsString())

        startTime = time.time()
        while time.time() - startTime < Config.timePerRun:
            offspring = population.generateOffspring()
            population.individuals = population.selectBest(offspring, Config.populationSize)

            best = population.selectBest([best], 1)[0]
            allPopulations.append(population.getIndividualsString())

        return allPopulations, best

    @staticmethod
    def frequencyAssignmentMemeticAlgorithm():
        allPopulations = []
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(Config.populationSize)
        best = population.selectBest([], 1)[0]
        allPopulations.append(population.getIndividualsString())

        startTime = time.time()
        while time.time() - startTime < Config.timePerRun:
            offspring = population.generateOffspring()
            population.individuals = population.selectLeastFrequent(offspring, Config.populationSize)

            best = population.selectBest([best], 1)[0]
            allPopulations.append(population.getIndividualsString())

        return allPopulations, best

    @staticmethod
    def hillClimberAlgorithm(instance, name, run, functionEvaluations, startSequence):
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(1, instance)
        if startSequence is not None:
            population.individuals = [SimpleEncoding(startSequence, instance)]
        best = population.individuals[0]
        Algorithm.writeBestToFile(name, run, best.getObjectiveValue(), True)

        while functionEvaluations < Config.maxFunctionEvaluations:
            if functionEvaluations % 1000000 == 0:
                print("Normal: On function evaluation " + str(functionEvaluations) + " for instance " + name + " in run " + str(run))
            newIndividual = population.individuals[0].randomSingleSwap()

            best = population.selectBest([best, newIndividual], 1)[0]

            population.individuals = population.selectBestPreferOffspring([newIndividual])

            functionEvaluations += 1
            if functionEvaluations % 1000 == 0:
                Algorithm.writeBestToFile(name, run, best.getObjectiveValue(), False)
                Algorithm.writeCurrentToFile(name, run, False, functionEvaluations, population.individuals[0].sequence)

        return best

    @staticmethod
    def frequencyAssignmentHillClimberAlgorithm(instance, name, run, functionEvaluations, startSequence, best, frequency):
        population = GenotypeFactory.generateRandomSimpleEncodingPopulation(1, instance)
        if startSequence is not None:
            population.individuals = [SimpleEncoding(startSequence, instance)]
        if frequency is not None:
            population.frequency = frequency
        if best == 0:
            best = population.individuals[0].getObjectiveValue()
        Algorithm.writeBestToFile(name, run, best, True)

        while functionEvaluations < Config.maxFunctionEvaluations:
            if functionEvaluations % 1000000 == 0:
                print("FFA: On function evaluation " + str(functionEvaluations) + " for instance " + name + " in run " + str(run))
            newIndividual = population.individuals[0].randomSingleSwap()

            if newIndividual.getObjectiveValue() < best:
                best = newIndividual.getObjectiveValue()

            population.individuals = population.selectLeastFrequentPreferOffspring([newIndividual])

            functionEvaluations += 1
            if functionEvaluations % 1000 == 0:
                Algorithm.writeBestToFile(name, run, best, True)
                Algorithm.writeCurrentToFile(name, run, True, functionEvaluations, population.individuals[0].sequence, population.frequency)

        return best

    @staticmethod
    def writeBestToFile(name, run, value, ffa):
        if ffa:
            fileName = str(run) + "/" + name + "/fhc.txt"
        else:
            fileName = str(run) + "/" + name + "/hc.txt"

        os.makedirs(os.path.dirname('files/output/hc/populations/' + fileName), exist_ok=True)
        populationsWriteFile = open('files/output/hc/populations/' + fileName, 'a')
        populationsWriteFile.write(str(value) + ", ")

    @staticmethod
    def writeCurrentToFile(name, run, ffa, evals, sequence, frequency=None):
        if ffa:
            fileName = str(run) + "/" + name + "/current_fhc.txt"
            text = str(evals) + ", " + str(sequence) + "\n" + json.dumps(frequency)
        else:
            fileName = str(run) + "/" + name + "/current_hc.txt"
            text = str(evals) + ", " + str(sequence)

        os.makedirs(os.path.dirname('files/output/hc/populations/' + fileName), exist_ok=True)
        populationsWriteFile = open('files/output/hc/populations/' + fileName, 'w')
        populationsWriteFile.write(text)
