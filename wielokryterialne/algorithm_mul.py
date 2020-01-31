# RAW ALGORITHM
from deap import creator, base, tools, algorithms, benchmarks
import time
import migration as mig
import numpy
import pickle
import sys
import random
import benchmarks_conf as bc
import os
import nsga2_alg
import utils
from copy import deepcopy

# Przetwarzanie parametrów
# argv[0] to nazwa programu - tak jest domyślnie
# NAZWA BENCHMARKA - argv[1]
# LICZBA WYSP - argv[2]
# MNOŻNIK MIGRACJI - argv[3]
# MAX LICZBA WYWOŁAŃ BEZ POPRAWY - argv[4]
# MODEL - argv[5]

if(len(sys.argv) != 7):
    print("Wrong number of arguments!")
    print("Usage:", sys.argv[0],
          "BENCHMARK_NAME NUM_OF_ISLANDS MIGRATIONS_RATIO max_iterations_wo_improvement MODEL NUM_OF_OBJECTIVES")
    sys.exit()


# nazwa benchmarka
BENCHMARK_NAME = sys.argv[1]

# Początkowa liczba wysp
NUM_OF_ISLANDS = int(sys.argv[2])

# Mnożnik migracji
MIGRATION_RATIO = float(sys.argv[3])

# max liczba wywołań bez poprawy
max_iterations_wo_improvement = int(sys.argv[4])

# model
MODEL = sys.argv[5]

NUM_OF_OBJECTIVES = int(sys.argv[6])


POPULATION_SIZE = 100
ISLAND_POPULATION_SIZE = int(POPULATION_SIZE / NUM_OF_ISLANDS)
FREQ = int(MIGRATION_RATIO * POPULATION_SIZE)
CXPB, MUTPB = 0.1, 1.0


if(BENCHMARK_NAME == "dtlz1"):
    toolbox = bc.getDTLZ1ToolBox(NUM_OF_OBJECTIVES)

if(BENCHMARK_NAME == "dtlz2"):
    toolbox = bc.getDTLZ2ToolBox(NUM_OF_OBJECTIVES)

if(BENCHMARK_NAME == "dtlz3"):
    toolbox = bc.getDTLZ3ToolBox(NUM_OF_OBJECTIVES)

if(BENCHMARK_NAME == "dtlz4"):
    toolbox = bc.getDTLZ4ToolBox(NUM_OF_OBJECTIVES)


toolbox.register("map", map)


# Migrate method
if(MODEL == "convection_const"):
    toolbox.register("migrate", mig.migSelFrontsContsInslands,
                     numOfIslands=NUM_OF_ISLANDS)

if(MODEL == "convection_front"):
    toolbox.register("migrate", mig.migSelOneFrontOneIsland)

if(MODEL == "island"):
    toolbox.register("migrate", mig.migIslandsRandom,
                     numOfIslands=NUM_OF_ISLANDS)

# Statistics
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean, axis=0)
stats.register("std", numpy.std, axis=0)
stats.register("min", numpy.min, axis=0)
stats.register("max", numpy.max, axis=0)


# Zapisuje n najlepszych osobników (tutaj n = 1)
#hallOfFame = tools.ParetoFront()

hallOfFame = nsga2_alg.myParetoFront(100)

# ngen = FREQ oznacza ile wykonań algorytmu się wykona przy jednym uruchomieniu funkcji
toolbox.register("algorithm", nsga2_alg.nsga2Algorithm, toolbox=toolbox,
                 stats=stats, cxpb=CXPB, mutpb=MUTPB, ngen=FREQ, verbose=False, halloffame=hallOfFame)

logbooks = []

bestIndividuals = []
start_time = time.time()
iterations_wo_improvement = 0

# Początkowa populacja
islands = [toolbox.population(n=ISLAND_POPULATION_SIZE)
           for i in range(NUM_OF_ISLANDS)]

toolbox.migrate(islands)


first = True
previous_pareto_front = None

print("Running:", BENCHMARK_NAME)
print("Islands number:", NUM_OF_ISLANDS)
print("Migration every", FREQ, "steps")
print("Max iterations without improvement:", max_iterations_wo_improvement)
print("Model:", MODEL)
print("----------START---------")
mig_start_time = time.time()
while(iterations_wo_improvement <= max_iterations_wo_improvement / FREQ):

    results = toolbox.map(toolbox.algorithm, islands)

    ziped = list(map(list, zip(*results)))
    islands = ziped[0]

    removed = ziped[2]

    sum_removed = sum(removed)

    if(sum_removed <= 1):
        iterations_wo_improvement += 1
    else:
        iterations_wo_improvement = 0
        print("Removed: ", sum_removed,
              "Improvement: ", hallOfFame[0].fitness)

    if(iterations_wo_improvement * FREQ % int(max_iterations_wo_improvement / 10) == 0):
        print("iterations_wo_improvement:", (iterations_wo_improvement *
                                             FREQ / max_iterations_wo_improvement) * 100, "%  time:", round(time.time() - mig_start_time, 2))
        mig_start_time = time.time()

    bestInMigration = []
    for ind in hallOfFame:
        bestInMigration.append(ind.fitness.values)

    bestIndividuals.append(bestInMigration)

    if first:
        for logbook in ziped[1]:
            logbooks.append(logbook)
        first = False
    else:
        for k, logbook in enumerate(ziped[1]):
            logbooks[k] += logbook

    toolbox.migrate(islands)


print("----------END---------")
print("Hall of fame[0]:", hallOfFame[0], hallOfFame[0].fitness)

# Save results
pickleOut = open("./out/" + BENCHMARK_NAME + "_" + str(NUM_OF_ISLANDS) +
                 "_" + str(MIGRATION_RATIO) + "_" + MODEL + "_" + str(NUM_OF_OBJECTIVES) + ".pickle", "wb")
pickle.dump(utils.result(
    logbooks, bestIndividuals, time.time() - start_time), pickleOut)
pickleOut.close()

print("\n")
