from __future__ import division
import random
from deap import tools, creator
import statistics
# sortuje według fitness niemalejąco
# do selekcji konwekcyjnej dla problemów jednokryterialnych


def sortByFitness(wholePopulation):
    wholePopulation.sort(key=lambda x: x.fitness, reverse=False)

# Migracja frontami pareto ze stałą liczbą wysp


def migSelFrontsContsInslands(populations, numOfIslands):
    wholePopulation = []

    for population in populations:
        wholePopulation += population

    pareto_fronts = tools.sortNondominated(
        wholePopulation, len(wholePopulation))

    wholePopulation = []

    for population in pareto_fronts:
        wholePopulation += population

    islandSize = int(len(wholePopulation) / numOfIslands)

    newIslands = []

    for i in range(0, len(wholePopulation), islandSize):
        newIslands.append(wholePopulation[i:i + islandSize])
        lastIndex = i + islandSize

    newIslands[-1] += wholePopulation[lastIndex:]

    for i, newIs in enumerate(newIslands):
        if(i >= len(populations)):
            populations.append(newIs)
        else:
            populations[i] = newIs

    if(len(populations) > len(newIslands)):
        del populations[len(newIslands):]

# Migracja między wyspami w selekcji konwekcyjnej dla problemów WIELOKRYTERIALNYCH


def migSelOneFrontOneIsland(populations):
    wholePopulation = []

    for population in populations:
        wholePopulation += population

    pareto_fronts = tools.sortNondominated(
        wholePopulation, len(wholePopulation))

    for i, newIs in enumerate(pareto_fronts):
        if(i >= len(populations)):
            populations.append(newIs)
        else:
            populations[i] = newIs

    if(len(populations) > len(pareto_fronts)):
        del populations[len(pareto_fronts):]

# Migracja między wyspami w selekcji konwekcyjnej dla problemów JEDNOKRYTERIALNYCH


def migSel(populations, numOfIslands):
    wholePopulation = []

    for population in populations:
        wholePopulation += population

    islandSize = int(len(wholePopulation) / numOfIslands)

    newIslands = []

    sortByFitness(wholePopulation)

    for i in range(0, len(wholePopulation), islandSize):
        newIslands.append(wholePopulation[i:i + islandSize])
        lastIndex = i + islandSize

    newIslands[-1] += wholePopulation[lastIndex:]

    for i, newIs in enumerate(newIslands):
        if(i >= len(populations)):
            populations.append(newIs)
        else:
            populations[i] = newIs

    if(len(populations) > len(newIslands)):
        del populations[len(newIslands):]


def migIslandsRandom(populations, numOfIslands):
    wholePopulation = []

    for population in populations:
        wholePopulation += population

    islandSize = int(len(wholePopulation) / numOfIslands)

    newIslands = []

    random.shuffle(wholePopulation)

    for i in range(0, len(wholePopulation), islandSize):
        newIslands.append(wholePopulation[i:i + islandSize])
        lastIndex = i + islandSize

    newIslands[-1] += wholePopulation[lastIndex:]

    for i, newIs in enumerate(newIslands):
        if(i >= len(populations)):
            populations.append(newIs)
        else:
            populations[i] = newIs

    if(len(populations) > len(newIslands)):
        del populations[len(newIslands):]
