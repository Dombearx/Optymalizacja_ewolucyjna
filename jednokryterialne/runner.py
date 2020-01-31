from subprocess import call

num_of_iterations = ["10000"]

num_of_islands = ["5", "10"]
migration_ratio = ["2", "10", "20"]

models = [
    "convection",
    "island"
]

benchmarks = [
    "h1",
    "ackley",
    "himmelblau",
    "schwefel",
    "rastrigin"
]

for model in models:
    for benchmarkName in benchmarks:
        for islandNum in num_of_islands:
            for ratio in migration_ratio:
                for maxIterations in num_of_iterations:
                    call(["python", "algorithm.py", benchmarkName, islandNum,
                          ratio, maxIterations, model])
