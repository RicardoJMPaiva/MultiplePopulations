import json
params = {
    "PROB_MUTATION": 0.1,
    "PROB_CROSSOVER": 0.9,
    "NR_GENERATIONS": 100,
    "NR_INDIVIDUALS": 500,
    "TOURNAMENT": 3,  # tournament size
    "ELITISM": 10,    # number of individuals
    "NR_CUTS": 1,
    "SIZE_GENOTYPE": 250,    # NR ITEMS of problem
    "METHOD": 2,      # 0 - SGA 1 - Multi-populations 2 - Random Immigrants
    "INDIVIDUALS_REPLACE": 25,  # number of individuals to replace - Random Immigrants
    "INDIVIDUALS_EXCHANGE": 375,  # number of individuals to exchange - Multi populations
    "EXCHANGE_METHOD": "worst",      # worst, best, random -  Multi populations
    "MIGRATION": 5,      # 1 - always, 2 - each 2 generations, 3 - each X gen, a partir de X
    "PERTURBATION": 10, # each 10 generations (needs to be the number that the problem used)
}

with open('datasets/dataset2.json') as f:
  data = json.load(f)

pasta = "save/B/dataset2/0.75_5/"
experimentation = {
    "NR_EXP": 30,
    "SAVE_FOLDER": pasta,
    "SAVE_FILE": pasta + "best.txt",
    "SAVE_FILE2": pasta + "best2.txt",
    "SAVE_POP": pasta + "log/",
    "PROBLEM_DATASET": data,
    "PROBLEM": data[0],
    "PERTUB": 0,      # auxiliar variable - don't change
    "FITNESS": "linear"    # linear, quadratic, zero
}