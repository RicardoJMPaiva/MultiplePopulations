from utils import *

params = {
    "PROB_MUTATION": 0.1,
    "PROB_CROSSOVER": 0.9,
    "NR_GENERATIONS": 100,
    "NR_INDIVIDUALS": 1000,
    "TOURNAMENT": 3,
    "ELITISM": 10,
    "NR_CUTS": 1,
    "SIZE_GENOTYPE": kp["NR_ITEMS"],    # NR ITEMS
    "METHOD": 1,
    "INDIVIDUALS_REPLACE": 3,
    "INDIVIDUALS_EXCHANGE": 5,
    "EXCHANGE_METHOD": "random",      # worst, best, random
    "MIGRATION": 1,      # 1 - always, 2 - each 2 generations, 3 - each X gen, a partir de X
    "MIGRATION_N": 5,
}


experimentation = {
    "NR_EXP": 1,
    "SAVE_FILE": "save/logs.txt",
    "PROBLEM": generate_weak_cor(),
    "FITNESS": "quadratic"    # linear, quadratic, zero
}