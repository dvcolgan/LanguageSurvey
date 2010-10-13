import random
from farkle import GAPlayer, Farkle

class FarkleProblem(object):
    def create_random_individual(self):
        return GAPlayer()

    def run_tournament(self, p1, p2):
        game = Farkle()
        game.add_player(p1)
        game.add_player(p2)

        p1_wins, p2_wins = 0, 0
        for i in range(10):
            winner = game.play()
            if winner == 0: p1_wins += 1
            if winner == 1: p2_wins += 1
        if p1_wins >= p2_wins: return p1
        if p1_wins <  p2_wins: return p2


    def mate_individuals(self, i1, i2):
        pivot = random.randint(0,9)
        child1 = i1.gene[:pivot] + i2.gene[pivot:]
        child2 = i2.gene[:pivot] + i1.gene[pivot:]
        return GAPlayer(child1), GAPlayer(child2)

    def mutate_individual(self, ind, mutation_rate):
        if random.random() < mutation_rate:
            print 'mutated'
            pivot = random.randint(0,9)
            if pivot == 0: ind.gene[pivot] = randint(0,1)
            elif pivot == 1: ind.gene[pivot] = randint(0,1)
            elif pivot == 2: ind.gene[pivot] = randint(0,1)
            elif pivot == 3: ind.gene[pivot] = randint(0,1)
            elif pivot == 4: ind.gene[pivot] = randint(0,1)
            elif pivot == 5: ind.gene[pivot] = randint(0,1)
            elif pivot == 6: ind.gene[pivot] = randint(0,2)
            elif pivot == 7: ind.gene[pivot] = randint(0,2)
            elif pivot == 8: ind.gene[pivot] = randint(0,2)
            elif pivot == 9: ind.gene[pivot] = randint(0,2)
            elif pivot == 10: ind.gene[pivot] = randint(0,2)
            elif pivot == 11: ind.gene[pivot] = randint(0,2)
            elif pivot == 12: ind.gene[pivot] = randint(0,1)
            elif pivot == 13: ind.gene[pivot] = randint(0,1)
            elif pivot == 14: ind.gene[pivot] = randint(0,1)
            elif pivot == 15: ind.gene[pivot] = randint(0,2)
            elif pivot == 16: ind.gene[pivot] = randint(0,2)
            elif pivot == 17: ind.gene[pivot] = randint(0,2)
            elif pivot == 18: ind.gene[pivot] = randint(0,2)
            elif pivot == 19: ind.gene[pivot] = randint(0,2)
            elif pivot == 20: ind.gene[pivot] = randint(0,2)
            elif pivot == 21: ind.gene[pivot] = randint(0,2)
            elif pivot == 22: ind.gene[pivot] = randint(0,2)
            elif pivot == 23: ind.gene[pivot] = randint(0,2)
            elif pivot == 24: ind.gene[pivot] = randint(0,2)
            elif pivot == 25: ind.gene[pivot] = randint(0,2)
            elif pivot == 26: ind.gene[pivot] = randint(0,2)
            elif pivot == 27: ind.gene[pivot] = randint(0,1)
            elif pivot == 28: ind.gene[pivot] = randint(0,1)
            elif pivot == 29: ind.gene[pivot] = randint(0,1)
            elif pivot == 30: ind.gene[pivot] = random.choice(range(0, 3501, 50))
            elif pivot == 30: ind.gene[pivot] = random.choice(range(0, 3501, 50))
            elif pivot == 30: ind.gene[pivot] = random.choice(range(0, 3501, 50))
            elif pivot == 30: ind.gene[pivot] = random.choice(range(0, 3501, 50))
            elif pivot == 30: ind.gene[pivot] = random.choice(range(0, 3501, 50))
            elif pivot == 30: ind.gene[pivot] = random.choice(range(0, 3501, 50))
        return ind


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

    def find_strongest_individual(self):
        pool = list(self.population)
        winners = []
        while len(pool) > 1:
            for i in range(0, len(pool), 2):
                print i
                individual1, individual2 = pool[i], pool[i+1]
                winner = self.problem_manager.run_tournament(individual1,
                                                             individual2)
                winners.append(winner)
            pool = winners
            winners = []
        print pool[0].gene


    def print_report(self):
        for individual in self.population:
            print individual.gene

    def run(self):
        self.generate_random_population()
        for i in range(self.max_generations):
            print 'generation',  i
            self.hold_binary_tournament()
            self.do_crossover()
            self.do_mutation()
            if self.is_converged(): break
            self.print_report()
        self.find_strongest_individual()


if __name__ == "__main__":
    print 'starting'
    ga = GA(FarkleProblem(), population_size=16, max_generations=2)
    ga.run()
    print 'done'
