import array
import random
import json
import time


import numpy

from math import sqrt

from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools
from operator import eq
from copy import deepcopy


class myParetoFront():

    def __init__(self, maxLen, similar=eq):
        self.keys = list()
        self.items = list()
        self.maxLen = maxLen
        self.similar = similar

    def insert(self, item):
        item = deepcopy(item)

        self.items.append(item)
        self.keys.append(item.fitness)

    def remove(self, index):

        del self.keys[index]
        del self.items[index]

    def replace(self, index, item):
        item = deepcopy(item)

        self.keys[index] = item
        self.items[index] = item.fitness

    def update(self, population):

        removed = 0

        for ind in population:
            is_dominated = False
            dominates_one = False
            has_twin = False
            to_remove = []
            for i, hofer in enumerate(self):    # hofer = hall of famer
                if not dominates_one and hofer.fitness.dominates(ind.fitness):
                    is_dominated = True
                    break
                elif ind.fitness.dominates(hofer.fitness):
                    dominates_one = True
                    to_remove.append(i)
                elif ind.fitness == hofer.fitness and self.similar(ind, hofer):
                    has_twin = True
                    break

            for i in reversed(to_remove):       # Remove the dominated hofer
                self.remove(i)
                removed += 1
            if not is_dominated and not has_twin:
                if(len(self) < self.maxLen):
                    self.insert(ind)

        return removed

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        return self.items[i]

    def __iter__(self):
        return iter(self.items)

    def __reversed__(self):
        return reversed(self.items)

    def __str__(self):
        return str(self.items)


def nsga2Algorithm(population, toolbox, cxpb, mutpb, ngen, stats=None, halloffame=None, verbose=__debug__):

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    numOfIndividuals = len(population)

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    population = toolbox.select(population, len(population))

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, evals=len(invalid_ind), **record)

    if verbose:
        print(logbook.stream)
    # Begin the generational process

    removed = 0
    for gen in range(1, ngen + 1):
        # Vary the population

        # Dodawanie osobników aż populacja będzie podzielna przez 4
        while(len(population) % 4 != 0):
            population.append(
                population[random.randint(0, len(population) - 1)])

        offspring = tools.selTournamentDCD(population, len(population))

        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= cxpb:
                ind1, ind2 = toolbox.mate(ind1, ind2)

            if random.random() <= mutpb:
                toolbox.mutate(ind1)
            if random.random() <= mutpb:
                toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        if halloffame is not None:
            removed += halloffame.update(offspring)

        # Select the next generation population
        population = toolbox.select(population + offspring, numOfIndividuals)
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)
    return population, logbook, removed
