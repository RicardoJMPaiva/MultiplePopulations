"""
    Multi-population and Random Immigrants algorithms
    Evolutionary Computation, 2020, UC, DEI
    Master of Informatics Engineering
"""
__author__ = 'Jessica Cunha, Ricardo Paiva'
__date__ = 'May 2020'

from parameters import *
from Individual import *
import random
import copy
import math
import json
import os

def generate_genotype():
    """ Function that genarates the genotype of the individual """
    gen = []
    for _ in range(params["SIZE_GENOTYPE"]):
        gen.append(random.randint(0,1))
    return gen

def genotype_to_phenotype(genotype):
    """ Function that does the mapping of the genotype into the phenotype"""
    problem = experimentation["PROBLEM"]
    phenotype = []
    for i in range(len(genotype)):
        if genotype[i] == 1:
            phenotype.append([i,problem['weights'][i], problem['values'][i]])
    return phenotype

def fitness(population):
    """ Function that calculates the fitness of the whole population"""
    problem = experimentation["PROBLEM"]
    capacity = problem["capacity"]
    for ind in population:
        total_weight = 0.0
        fitness = 0.0
        for _, w, v in ind.get_phenotype():
            total_weight += w
            fitness += v
        if total_weight > capacity:
            if experimentation["FITNESS"] == "log":
                rho = max([v/w for i,w,v in ind.get_phenotype()])
                fitness -= math.log(1 + rho * (total_weight - capacity),2)
            elif experimentation["FITNESS"] == "quadratic":
                rho = max([v/w for i,w,v in ind.get_phenotype()])
                fitness -=  (rho * (total_weight - capacity))**2
            elif experimentation["FITNESS"] == "linear":
                rho = max([v/w for i,w,v in ind.get_phenotype()])
                fitness -=  rho * (total_weight - capacity)
            elif experimentation["FITNESS"] == "zero":
                return 0
            else:
                print("FITNESS FUNCTION DOESNT EXIST")
        ind.set_fitness(fitness)
def mutation(ind):
    " Random resetting mutation"
    gen = copy.deepcopy(ind.get_genotype())

    for i in range(params['SIZE_GENOTYPE']):
        if random.random() < params['PROB_MUTATION']:
            gen[i] = random.randint(0,1)
    fen = genotype_to_phenotype(gen)
    new_ind = Individual(gen, fen)
    return new_ind

def crossover(ind1, ind2):
    """ N-point crossover """
    gen1 = copy.deepcopy(ind1.get_genotype())
    gen2 = copy.deepcopy(ind2.get_genotype())
    cuts = []
    while len(cuts) != params['NR_CUTS']:
        cutPoint = random.randint(0,params['SIZE_GENOTYPE'])
        if cutPoint not in cuts:
            cuts.append(cutPoint)
    cuts.sort()

    partnerGenotype = False
    start = 0
    for i in range(0, params['NR_CUTS']):
        if i != 0:
            start = cuts[i-1]
        partnerGenotype = not partnerGenotype
        if partnerGenotype:
            gen1[start:cuts[i]] = ind2.get_genotype()[start:cuts[i]]
            gen2[start:cuts[i]] = ind1.get_genotype()[start:cuts[i]]
    new_ind1 = Individual(gen1, genotype_to_phenotype(gen1))
    new_ind2 = Individual(gen2, genotype_to_phenotype(gen2))
    return new_ind1, new_ind2

def generate_population():
    """ Function to generate the population"""
    population = []
    for _ in range(params["NR_INDIVIDUALS"]):
        gen = generate_genotype()
        fen = genotype_to_phenotype(gen)
        ind = Individual(gen, fen)
        population.append(ind)
    return population

def tournament(population):
    """ Tournament selection """
    pool = random.sample(population, params['TOURNAMENT'])
    pool.sort(key=lambda i: i.get_fitness(),reverse=True)
    return copy.deepcopy(pool[0])

def worst_replacement(population):
    """
    Random immigrants function
    Replaces the worst individuals of the population by new randomly generated
    """
    population.sort(key=lambda x: x.get_fitness(),reverse=True)
    total = len(population) - params["INDIVIDUALS_REPLACE"]
    new_population = population[:total]
    for _ in range(params["INDIVIDUALS_REPLACE"]):
        gen = generate_genotype()
        new_population.append(Individual(gen, genotype_to_phenotype(gen)))
    fitness(new_population)
    return new_population

def select_random_idx(pop):
    """
    Auxiliar function to select random individuals
    """
    ix = []
    while len(ix) < params["INDIVIDUALS_EXCHANGE"]:
        ind = random.randint(0,len(pop) - 1)
        if ind not in ix:
            ix.append(ind)
    ix.sort(reverse=True)
    return ix

def exchange_random(pop1,pop2):
    """
    Auxiliary function for the Multi-populations algorithm
    Exchange random individual's method
    """
    ix1 = select_random_idx(pop1)
    ix2 = select_random_idx(pop2)
    ind1 = []
    ind2 = []
    for index in ix1:
        ind1.append(pop1[index])
        del(pop1[index])

    for index in ix2:
        ind2.append(pop2[index])
        del(pop2[index])
 
    for i in range( params["INDIVIDUALS_EXCHANGE"]):
        pop1.append(ind2[i])
        pop2.append(ind1[i])
    return pop1, pop2

def exchange_worst(pop1,pop2):
    """
    Auxiliary function for the Multi-populations algorithm
    Exchange worst individual's method
    """
    ind1 = pop1[-params["INDIVIDUALS_EXCHANGE"]:]
    pop1[-params["INDIVIDUALS_EXCHANGE"]:] = pop2[-params["INDIVIDUALS_EXCHANGE"]:]
    pop2[-params["INDIVIDUALS_EXCHANGE"]:] = ind1

    return pop1,pop2

def exchange_best(pop1,pop2):
    """
    Auxiliary function for the Multi-populations algorithm
    Exchange best individual's method
    """
    ind1 = pop1[:params["INDIVIDUALS_EXCHANGE"]]
    pop1[:params["INDIVIDUALS_EXCHANGE"]] = pop2[:params["INDIVIDUALS_EXCHANGE"]]
    pop2[:params["INDIVIDUALS_EXCHANGE"]] = ind1
    return pop1,pop2


def change_populations(pop1, pop2):
    """
    Function for the Multi-populations algorithm
    """
    pop1.sort(key=lambda x: x.get_fitness(),reverse=True)
    pop2.sort(key=lambda x: x.get_fitness(),reverse=True)

    if params["EXCHANGE_METHOD"] == "random":
        pop1,pop2 = exchange_random(pop1,pop2)
    elif params["EXCHANGE_METHOD"] == "worst":
        pop1,pop2 = exchange_worst(pop1,pop2)
    elif params["EXCHANGE_METHOD"] == "best":
        pop1,pop2 = exchange_best(pop1,pop2)
    else:
        print("ERROR: Any exchange population method choosed")
    return pop1, pop2

def save_population(l, population):
    """
    Auxiliary function to save all individual's fitness
    """
    pop = []
    for ind in population:
        pop.append(ind.get_fitness())
    l.append(pop)
    return l

def save(exp, l, l2 = None):
    """
    Auxiliary function to save all individuals from all generations fitness
    """
    if not os.path.exists(experimentation["SAVE_POP"]):
        os.makedirs(experimentation["SAVE_POP"],  exist_ok=True)
    open('%s/exp%d.json' % (experimentation["SAVE_POP"],exp), 'w').write(json.dumps(l))
    if l2:
        open('%s/exp%d.json' % (experimentation["SAVE_POP"],exp), 'w').write(json.dumps(l2))

def main(exp):
    population = generate_population()
    l1=[]
    if params["METHOD"] == 1:
        population2 = generate_population()
        f2 = open(experimentation['SAVE_FILE2'],"a")
        l2 = []

    best = None
    migration_flag = True
    f = open(experimentation['SAVE_FILE'],"a")
    experimentation["PERTUB"] = 0
    for i in range(params["NR_GENERATIONS"]):
        print(" ----- GEN %s ------" % i)
        if params["METHOD"] > 0:
            # each 2 generations
            if params["MIGRATION"] == 2:
                migration_flag = not migration_flag
            elif params["MIGRATION"] > 3:
                if i % params["MIGRATION"] == 0:
                    migration_flag = True
                else:
                    migration_flag = False
        if (i+1) % params["PERTURBATION"] == 0 and i + 1 < params["NR_GENERATIONS"] :
            print("\t\t***")
            experimentation["PERTUB"] += 1
            experimentation["PROBLEM"] = experimentation["PROBLEM_DATASET"][experimentation["PERTUB"]]
            
        fitness(population)
        l1 = save_population(l1,population)
        if params["METHOD"] == 1:
            fitness(population2)
            if migration_flag:
                population, population2 = change_populations(population, population2)
            population2.sort(key=lambda x: x.get_fitness(),reverse=True)
            best2 = copy.deepcopy(population2[0])
            l2 = save_population(l2, population2)
            new_population2 = population2[:params['ELITISM']]
        if params["METHOD"] == 2 and migration_flag:
            population = worst_replacement(population)

        population.sort(key=lambda x: x.get_fitness(),reverse=True)
        best = copy.deepcopy(population[0])
        # Elitism
        new_population = population[:params['ELITISM']]
        while len(new_population) < params['NR_INDIVIDUALS']:
            new_ind = tournament(population)
            # mutation
            if random.random() < params["PROB_MUTATION"]:
                new_ind = mutation(new_ind)
            # crossover
            if random.random() < params["PROB_CROSSOVER"]:
                new_ind2 = tournament(population)
                new_ind, new_ind2 = crossover(new_ind, new_ind2)
                new_population.append(new_ind2)
            new_population.append(new_ind)

            if params["METHOD"] == 1:
                new_ind = tournament(population2)
                # mutation
                if random.random() < params["PROB_MUTATION"]:
                    new_ind = mutation(new_ind)
                # crossover
                if random.random() < params["PROB_CROSSOVER"]:
                    new_ind2 = tournament(population2)
                    new_ind, new_ind2 = crossover(new_ind, new_ind2)
                    new_population2.append(new_ind2)
                new_population2.append(new_ind)

        print("POP 1: ", best.get_fitness())
        population = new_population
        s = '\n%d,%f' %(i,best.get_fitness())
        f.write(s)
        if params["METHOD"] == 1:
            print("POP 2: ", best2.get_fitness())
            population2 = new_population2
            s = '\n%d,%f' %(i,best2.get_fitness())
            f2.write(s)
    
    if params["METHOD"] == 1:
        # COMMENT THIS TO AVOID SAVING ALL INDIVIDUALS FITNESS
        # save(exp,l1,l2)
        f2.close()
    # COMMENT THIS TO AVOID SAVING ALL INDIVIDUALS FITNESS
    # else:
    #     save(exp,l1)
    f.close()

if __name__ == "__main__":
    if not os.path.exists(experimentation["SAVE_FOLDER"]):
        os.makedirs(experimentation["SAVE_FOLDER"],  exist_ok=True)

    f = open(experimentation['SAVE_FILE'],"w")
    f.write("generation,fitness")
    f.close()
    if params["METHOD"] == 1:
        f2 = open(experimentation['SAVE_FILE2'],"w")
        f2.write("generation,fitness")
        f2.close()
    for exp in range(experimentation["NR_EXP"]):
        main(exp)