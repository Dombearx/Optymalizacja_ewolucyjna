#  benchmarks
from deap import creator, base, tools, algorithms, benchmarks
import framsFunctions as ff
import time
import numpy
import pickle
import sys
import random

from itertools import repeat
try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequenc


def registerStandard(attributes, creator, evalFrams):

    toolbox = base.Toolbox()

    toolbox.register("attr_frams", ff.getSimpleGenotype)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_frams, attributes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evalFrams)
    toolbox.register("mate", ff.framsCrossover)
    toolbox.register("mutate", ff.framsMutate)

    toolbox.register("select", tools.selNSGA2)

    return toolbox


def getVelocityHeightToolBox():

    creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    attributes = 1

    def evalFrams(individual):
        return ff.framsEvaluate(individual)

    toolbox = registerStandard(attributes, creator, evalFrams)

    return toolbox
