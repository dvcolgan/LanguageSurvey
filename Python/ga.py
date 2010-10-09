import random
from farkle import FarkleTournament


#try to evolve the sequence 0-9
class SequenceProblem(object):
    def create_random_individual(self):
        return [random.randint(0,9) for i in range(10)]

    def run_tournament(self, p1, p2):
        p1_fitness, p2_fitness = 0, 0
        for i in range(10):
            if p1[i] == i: p1_fitness += 1
            if p2[i] == i: p2_fitness += 1

        if p1_fitness >= p2_fitness: return p1
        if p1_fitness <  p2_fitness: return p2

    def mate_individuals(self, seq1, seq2):
        pivot = random.randint(0,9)
        child1 = seq1[:pivot] + seq2[pivot:]
        child2 = seq2[:pivot] + seq1[pivot:]
        return child1, child2

    def mutate_individual(self, seq, mutation_rate):
        if random.random() < mutation_rate:
            pivot = random.randint(0,9)
            seq[pivot] = random.randint(0,9)
        return seq





class GA(object):
    def __init__(self, problem_manager, population_size=1000, max_generations=1000, mutation_rate=0.01, crossover_rate=0.8):
        self.population = []
        self.problem_manager = problem_manager
        self.population_size = population_size
        self.max_generations = max_generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.mating_pool = []

    def generate_random_population(self):
        self.population = [self.problem_manager.create_random_individual()
                for i in range(self.population_size)]

    def hold_binary_tournament(self):
        self.mating_pool = []
        for i in range(self.population_size):
            contestant1 = random.choice(self.population)
            contestant2 = random.choice(self.population)
            winner = self.problem_manager.run_tournament(contestant1,
                                                         contestant2)
            self.mating_pool.append(winner)
            
    def do_crossover(self):
        self.population = []
        for i in range(0, self.population_size, 2):
            individual1, individual2 = self.mating_pool[i], self.mating_pool[i+1]
            if random.random() < self.crossover_rate:
                self.population.extend(self.problem_manager.mate_individuals(individual1,individual2))
            else:
                self.population.extend((individual1, individual2))

    def do_mutation(self):
        for individual in self.population:
            if random.random() < self.mutation_rate:
                self.problem_manager.mutate_individual(individual, self.mutation_rate)

    def is_converged(self):
        return False

    def print_report(self):
        for individual in self.population:
            print individual

    def run(self):
        self.generate_random_population()
        for i in range(self.max_generations):
            print 'generation',  i
            self.hold_binary_tournament()
            self.do_crossover()
            self.do_mutation()
            if self.is_converged(): break
        self.print_report()


if __name__ == "__main__":
    print 'starting'
    ga = GA(SequenceProblem(), population_size=100)
    ga.run()
    print 'done'
