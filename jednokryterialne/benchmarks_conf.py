#  benchmarks
from deap import creator, base, tools, algorithms, benchmarks
import migration as mig
import time
import utils
import numpy
import pickle
import sys
import random

from itertools import repeat
try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequenc


def changedMutGaussian(individual, mu, sigma, index, upper_bound, lower_bound):
    individual[index] += random.gauss(mu, sigma)
    individual[index] = max(min(individual[index], upper_bound), lower_bound)
    return individual,


def randomMutGaussian(ind, mu, sigma, upper_bound, lower_bound):
    index = random.randint(0, len(ind)-1)

    return changedMutGaussian(ind, mu=mu, sigma=sigma, index=index, upper_bound=upper_bound, lower_bound=lower_bound)


def registerStandard(lower_bound, upper_bound, attributes, creator, evalBenchmark):

    toolbox = base.Toolbox()

    toolbox.register("attr_float", random.uniform, lower_bound, upper_bound)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, attributes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evalBenchmark)
    toolbox.register("mate", tools.cxUniform, indpb=0.5)
    toolbox.register("mutate", randomMutGaussian, mu=0,
                     sigma=(upper_bound - lower_bound)/10, upper_bound=upper_bound, lower_bound=lower_bound)

    toolbox.register("select", tools.selTournament, tournsize=3)

    return toolbox


def getH1ToolBox():

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    attributes = 2
    lower_bound = -100
    upper_bound = 100

    def evalBenchmark(individual):
        return benchmarks.h1(individual)

    toolbox = registerStandard(
        lower_bound, upper_bound, attributes, creator, evalBenchmark)

    return toolbox


def getAckleyToolBox():

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    attributes = 10
    lower_bound = -15
    upper_bound = 30

    def evalBenchmark(individual):
        return benchmarks.ackley(individual)

    toolbox = registerStandard(
        lower_bound, upper_bound, attributes, creator, evalBenchmark)

    return toolbox


def getHimmelblauToolBox():

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    attributes = 2
    lower_bound = -6
    upper_bound = 6

    def evalBenchmark(individual):
        return benchmarks.himmelblau(individual)

    toolbox = registerStandard(
        lower_bound, upper_bound, attributes, creator, evalBenchmark)

    return toolbox


def getSchwefelToolBox():

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    attributes = 10
    lower_bound = -500
    upper_bound = 500

    def evalBenchmark(individual):
        return benchmarks.schwefel(individual)

    toolbox = registerStandard(
        lower_bound, upper_bound, attributes, creator, evalBenchmark)

    return toolbox


def getRastriginToolBox():

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    attributes = 10
    lower_bound = -5.12
    upper_bound = 5.12

    def evalBenchmark(individual):
        return benchmarks.rastrigin(individual)

    toolbox = registerStandard(
        lower_bound, upper_bound, attributes, creator, evalBenchmark)

    return toolbox
