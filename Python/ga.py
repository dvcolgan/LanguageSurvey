import random
from farkle import GAPlayer, Farkle

def lists_are_same(lst1, lst2):
    for e1, e2 in zip(lst1, lst2):
        if e1 != e2:
            return False
    return True


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
        pivot = random.randint(0,len(i1.gene_mutator)-1)
        child1 = i1.gene[:pivot] + i2.gene[pivot:]
        child2 = i2.gene[:pivot] + i1.gene[pivot:]
        return GAPlayer(child1), GAPlayer(child2)

    def mutate_individual(self, ind, mutation_rate):
        pivot = random.randint(0,len(ind.gene_mutator)-1)
        ind.gene[pivot] = ind.gene_mutator[pivot]()
        return ind


#manually set the python random methods to do the same thing for tests

#make this into a test?
#run this problem every time we change the GA code

class SequenceIndividual(object):
    def __init__(self):
        self.gene = [random.randint(0,9) for i in range(10)]

class SequenceProblem(object):
    def create_random_individual(self):
        return SequenceIndividual()

    def run_tournament(self, p1, p2):
        p1_fitness, p2_fitness = 0, 0
        for i in range(10):
            if p1.gene[i] == i: p1_fitness += 1
            if p2.gene[i] == i: p2_fitness += 1

        if p1_fitness >= p2_fitness: return p1
        if p1_fitness <  p2_fitness: return p2

    def mate_individuals(self, seq1, seq2):
        pivot = random.randint(0,9)
        child1, child2 = SequenceIndividual, SequenceIndividual
        child1.gene = seq1.gene[:pivot] + seq2.gene[pivot:]
        child2.gene = seq2.gene[:pivot] + seq1.gene[pivot:]
        return child1, child2

    def mutate_individual(self, seq, mutation_rate):
        if random.random() < mutation_rate:
            pivot = random.randint(0,9)
            seq.gene[pivot] = random.randint(0,9)
        return seq





class GA(object):
    def __init__(self, problem_manager, population_size=128, max_generations=100, mutation_rate=0.01, crossover_rate=0.8):
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

    def find_converging_individual(self):
        #thanks to http://stackoverflow.com/questions/3957856/determine-if-a-python-list-is-95-the-same
        # first use the Boyer-Moore Majority Vote Algorithm to determine the
        # most common element, then count that element to determine if it makes
        # up 95% of the elements

        candidate_cnt = 0
        current_candidate = self.population[0]
        for ind in self.population:
            if lists_are_same(ind.gene, current_candidate.gene):
                candidate_cnt += 1
            else:
                candidate_cnt -= 1

            if candidate_cnt == 0:
                current_candidate = ind
                candidate_cnt = 1

        times_appearing = 0
        for ind in self.population:
            if lists_are_same(ind.gene, current_candidate.gene):
                times_appearing += 1

        convergence = (1.0 * times_appearing) / len(self.population)
        return convergence, current_candidate


    def find_strongest_individual(self):
        pool = list(self.population)
        winners = []
        while len(pool) > 1:
            for i in range(0, len(pool), 2):
                individual1, individual2 = pool[i], pool[i+1]
                winner = self.problem_manager.run_tournament(individual1,
                                                             individual2)
                winners.append(winner)
            pool = winners
            winners = []
        return pool[0]


    def print_report(self):
        for individual in self.population:
            print individual.gene

    def run(self):
        try:
            self.generate_random_population()
            for i in range(self.max_generations):
                print 'generation',  i
                self.hold_binary_tournament()
                self.do_crossover()
                self.do_mutation()
                convergence, most_common_ind = self.find_converging_individual()
                print convergence
                if convergence > 0.95:
                    print most_common_ind.gene
                    break
            else:
                print self.find_strongest_individual().gene
        except KeyboardInterrupt:
            print self.find_strongest_individual().gene


if __name__ == "__main__":
    print 'starting'
    ga = GA(FarkleProblem())
    ga.run()
    print 'done'
