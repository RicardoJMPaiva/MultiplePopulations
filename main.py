from parameters import *
from Individual import *
import random
import copy

# FIXME: ver se o problema e maximizacao ou minimizacao
# funcoes c logs
# metodos
# problema


def generate_genotype():
    # TODO binario, floats, depende do problema
    return 0

def genotypetofenotype():
    # funcao de mapeamento
    pass

def fitness():
    pass

def mutation(ind):
    # corre o fenotipo
    gen = ind.get_genotype()

    for i in range(params['SIZE_GENOTYPE']):
        if random.random() < params['PROB_MUTATION']:
            gen[i] = random.random()

    new_ind = Individual(gen)
    return new_ind

def crossover(ind1, ind2):
    gen1 = ind1.get_genotype()
    gen2 = ind2.get_genotype()

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
            gen1[start:cuts[i]] = gen2[start:cuts[i]]
            gen2[start:cuts[i]] = gen1[start:cuts[i]]
    new_ind1 = Individual(gen1)
    new_ind2 = Individual(gen2)
    return new_ind1, new_ind2

def generate_population():
    population = []
    for _ in range(params["NR_INDIVIDUALS"]):
        ind = Individual(generate_genotype())
        population.append(ind)
    return population

def tournament(population):
    pool = random.sample(population, params['TOURNAMENT'])
    pool.sort(key=lambda i: i.getFitness())
    return copy.deepcopy(pool[0])

def worst_replacement(population):
    population.sort(key=lambda x: x.getFitness())
    total = len(population) - params["INDIVIDUALS_REPLACE"]
    new_population = population[:total]
    for _ in range(params["INDIVIDUALS_REPLACE"]):
        new_population.append(Individual(generate_genotype()))
        # TODO atribuir fitness aos novos individuos
    # TODO checkar se sai com o tamanho certo
    # TODO checkar que removemos realmente os piores
    return new_population

def main():
    population = generate_population()
    best = None
    for _ in range(params["NR_GENERATIONS"]):
        # TODO atribuir fitness

        population.sort(key=lambda x: x.getFitness())
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
        population = new_population

if __name__ == "__main__":
    for _ in range(experimentation["NR_EXP"]):
        main()