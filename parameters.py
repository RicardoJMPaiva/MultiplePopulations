import json
params = {
    "PROB_MUTATION": 0.1,
    "PROB_CROSSOVER": 0.9,
    "NR_GENERATIONS": 100,
    "NR_INDIVIDUALS": 500,
    "TOURNAMENT": 3,
    "ELITISM": 10,
    "NR_CUTS": 1,
    "SIZE_GENOTYPE": 250,    # NR ITEMS
    "METHOD": 1,
    "INDIVIDUALS_REPLACE": 3,
    "INDIVIDUALS_EXCHANGE": 5,
    "EXCHANGE_METHOD": "random",      # worst, best, random
    "MIGRATION": 1,      # 1 - always, 2 - each 2 generations, 3 - each X gen, a partir de X
    "MIGRATION_N": 5,
    "PERTURBATION": 10, # frequencia each 10 generations
}

with open('datasets/dataset1.json') as f:
  data = json.load(f)

pasta = "save/random/"
experimentation = {
    "NR_EXP": 30,
    "SAVE_FOLDER": pasta,
    "SAVE_FILE": pasta + "best.txt",
    "SAVE_FILE2": pasta + "best2.txt",
    "SAVE_POP": pasta + "log/",
    "PROBLEM_DATASET": data,
    "PROBLEM": data[0],
    "PERTUB": 0,
    "FITNESS": "linear"    # linear, quadratic, zero
}