# RAW ALGORITHM
from deap import creator, base, tools, algorithms, benchmarks
import migration as mig
import time
import utils
import numpy
import pickle
import sys
import random
import benchmarks_conf as bc
import os

# Przetwarzanie parametrów
# argv[0] to nazwa programu - tak jest domyślnie
# NAZWA BENCHMARKA - argv[1]
# LICZBA WYSP - argv[2]
# MNOŻNIK MIGRACJI - argv[3]
# MAX LICZBA WYWOŁAŃ BEZ POPRAWY - argv[4]
# MODEL - argv[5]

if(len(sys.argv) != 6):
    print("Wrong number of arguments!")
    print("Usage:", sys.argv[0],
          "BENCHMARK_NAME NUM_OF_ISLANDS MIGRATIONS_RATIO max_iterations_wo_improvement MODEL")
    sys.exit()


# nazwa benchmarka
BENCHMARK_NAME = sys.argv[1]

# Początkowa liczba wysp
NUM_OF_ISLANDS = int(sys.argv[2])

# Mnożnik migracji
MIGRATION_RATIO = int(sys.argv[3])

# max liczba wywołań bez poprawy
max_iterations_wo_improvement = int(sys.argv[4])

# model
MODEL = sys.argv[5]


POPULATION_SIZE = 100
ISLAND_POPULATION_SIZE = int(POPULATION_SIZE / NUM_OF_ISLANDS)
FREQ = MIGRATION_RATIO * POPULATION_SIZE
CXPB, MUTPB = 0.1, 1


if(BENCHMARK_NAME == "h1"):
    toolbox = bc.getH1ToolBox()

if(BENCHMARK_NAME == "ackley"):
    toolbox = bc.getAckleyToolBox()

if(BENCHMARK_NAME == "himmelblau"):
    toolbox = bc.getHimmelblauToolBox()

if(BENCHMARK_NAME == "schwefel"):
    toolbox = bc.getSchwefelToolBox()

if(BENCHMARK_NAME == "rastrigin"):
    toolbox = bc.getRastriginToolBox()


toolbox.register("map", map)


# Migrate method
if(MODEL == "convection"):
    toolbox.register("migrate", mig.migSel, numOfIslands=NUM_OF_ISLANDS)

if(MODEL == "island"):
    toolbox.register("migrate", mig.migIslandsRandom,
                     numOfIslands=NUM_OF_ISLANDS)

# Statistics
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)


# Zapisuje n najlepszych osobników (tutaj n = 1)
hallOfFame = tools.HallOfFame(1)

# ngen = FREQ oznacza ile wykonań algorytmu się wykona przy jednym uruchomieniu funkcji
toolbox.register("algorithm", algorithms.eaSimple, toolbox=toolbox,
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
previous_fitness = None


print("Running:", BENCHMARK_NAME)
print("Islands number:", NUM_OF_ISLANDS)
print("Migration every", FREQ, "steps")
print("Max iterations without improvement:", max_iterations_wo_improvement)
print("Model:", MODEL)
print("----------START---------")
while(iterations_wo_improvement <= max_iterations_wo_improvement / FREQ):

    results = toolbox.map(toolbox.algorithm, islands)

    ziped = list(map(list, zip(*results)))
    islands = ziped[0]

    # Jeżeli znajdzie lepszego osobnika niż najlepszy obecnie, to nadpisuje go

    if previous_fitness == None:
        previous_fitness = hallOfFame[0].fitness.values

    if previous_fitness == hallOfFame[0].fitness.values:
        iterations_wo_improvement += 1
    else:
        print("improvement after:", (iterations_wo_improvement + 1) *
              FREQ, "Fitness:", hallOfFame[0].fitness.values[0])
        iterations_wo_improvement = 0

        previous_fitness = hallOfFame[0].fitness.values

    if(iterations_wo_improvement * FREQ == int(max_iterations_wo_improvement / 2)):
        print(iterations_wo_improvement * FREQ,
              "iterations without improvement...")
    bestIndividuals.append(hallOfFame[0].fitness.values)

    if first:
        for logbook in ziped[1]:
            logbooks.append(logbook)
        first = False
    else:
        for k, logbook in enumerate(ziped[1]):
            logbooks[k] += logbook

    toolbox.migrate(islands)


print("----------END---------")
print("Hall of fame:", hallOfFame[0], hallOfFame[0].fitness)

# Save results
pickleOut = open("./out/" + BENCHMARK_NAME + "_" + str(NUM_OF_ISLANDS) +
                 "_" + str(MIGRATION_RATIO) + "_" + MODEL + ".pickle", "wb")
pickle.dump(utils.result(
    logbooks, bestIndividuals, time.time() - start_time), pickleOut)
pickleOut.close()

print("\n")
