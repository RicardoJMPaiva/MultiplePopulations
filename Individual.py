

class Individual:
    def __init__(self, genotype):
        self.genotype = genotype
        self.phenotype = None
        self.fitness = None

    def get_fitness(self):
        return self.fitness

    def set_fitness(self, fitness):
        self.fitness = fitness

    def get_genotype(self):
        return self.genotype
