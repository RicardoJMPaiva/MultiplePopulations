from parameters import *
from Individual import *
import random
import copy
import math
import copy

# FIXME: ver se o problema e maximizacao ou minimizacao
# funcoes c logs
# metodos
# problema: Knapsack
# TODO ao atualizar o problema, atualizar nos parametros, ou mandar como argumento

def generate_genotype():
    gen = []
    for _ in range(params["SIZE_GENOTYPE"]):
        gen.append(random.randint(0,1))
    return gen

def genotype_to_fenotype(genotype):
    problem = experimentation["PROBLEM"]
    phenotype = []
    for i in range(len(genotype)):
        if genotype[i] == 1:
            phenotype.append([i,problem['weights'][i], problem['values'][i]])
    return phenotype

def fitness(population):
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
    # corre o fenotipo
    gen = copy.deepcopy(ind.get_genotype())

    for i in range(params['SIZE_GENOTYPE']):
        if random.random() < params['PROB_MUTATION']:
            gen[i] = random.randint(0,1)
    fen = genotype_to_fenotype(gen)
    new_ind = Individual(gen, fen)
    return new_ind

def crossover(ind1, ind2):
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
    new_ind1 = Individual(gen1, genotype_to_fenotype(gen1))
    new_ind2 = Individual(gen2, genotype_to_fenotype(gen2))
    return new_ind1, new_ind2

def generate_population(problem):
    population = []
    for _ in range(params["NR_INDIVIDUALS"]):
        gen = generate_genotype()
        fen = genotype_to_fenotype(gen)
        ind = Individual(gen, fen)
        population.append(ind)
    return population

def tournament(population):
    pool = random.sample(population, params['TOURNAMENT'])
    pool.sort(key=lambda i: i.get_fitness(),reverse=True)

    return copy.deepcopy(pool[0])

def worst_replacement(population):
    population.sort(key=lambda x: x.get_fitness(),reverse=True)
    total = len(population) - params["INDIVIDUALS_REPLACE"]
    new_population = population[:total]
    for _ in range(params["INDIVIDUALS_REPLACE"]):
        gen = generate_genotype()
        new_population.append(Individual(gen, genotype_to_fenotype(gen)))
        # TODO atribuir fitness aos novos individuos
    # TODO checkar se sai com o tamanho certo
    # TODO checkar que removemos realmente os piores
    fitness(new_population)
    return new_population

def main():
    population = generate_population(experimentation["PROBLEM"])
    best = None
    for _ in range(params["NR_GENERATIONS"]):
        problem = experimentation["PROBLEM"]
        # TODO variar capacidade a cada geracao
        fitness(population)

        population.sort(key=lambda x: x.get_fitness(),reverse=True)
        best = copy.deepcopy(population[0])

        if params["METHOD"] == 2:
            # TODO ver onde ficar melhor
            # TODO flag c a frequencia de imigracao
            population = worst_replacement(population)

        # Elitism
        new_population = population[:params['ELITISM']]
        while len(new_population) < params['NR_INDIVIDUALS']:
            # TOURNAMENT
            new_ind = tournament(population)
            # FIXME ver a seed
            # mutation
            if random.random() < params["PROB_MUTATION"]:
                new_ind = mutation(new_ind)
            # crossover
            if random.random() < params["PROB_CROSSOVER"]:
                new_ind2 = tournament(population)
                # retornar 1 ou 2
                new_ind, new_ind2 = crossover(new_ind, new_ind2)
                new_population.append(new_ind2)

            new_population.append(new_ind)
        print(best.get_fitness())
        population = new_population

if __name__ == "__main__":
    for _ in range(experimentation["NR_EXP"]):
        main()