import random

import numpy
from Genetic import GA_LAB1
import matplotlib.pyplot as plt


def plot(cf, icf, learning, gen):
    print(learning)
    plt.plot(gen, learning, label="learning bits")
    plt.ylabel('learning bits')
    plt.xlabel('generations')
    plt.title('learning bits percentage')
    plt.legend()
    plt.show()

    plt.plot(gen, cf, label="Correctly Fixed")

    plt.ylabel('Correctly Fixed')
    plt.xlabel('generations')
    plt.title('Correctly Fixed')
    plt.legend()
    plt.show()

    plt.plot(gen, icf, label="inCorrectly Fixed")

    plt.ylabel('inCorrectly Fixed')
    plt.xlabel('generations')
    plt.title('inCorrectly Fixed')
    plt.legend()
    plt.show()

    plt.plot(gen, learning, label="learning bits")
    plt.plot(gen, cf, label="Correctly Fixed")
    plt.plot(gen, icf, label="inCorrectly Fixed")

    plt.xlabel('inCorrectly Fixed')
    plt.ylabel('generations')
    plt.title('Together')
    plt.legend()
    plt.show()


class PureMA(GA_LAB1):
    def __init__(self, target, tar_size, pop_size, problem_spec, crosstype, fitnesstype, selection,
                 serviving_mechanizem, mutation, gene_dist,k=0, mutation_probability=0):
        GA_LAB1.__init__(self, target, tar_size, pop_size, problem_spec, crosstype, fitnesstype, selection,
                         serviving_mechanizem, mutation, gene_dist, 0)
        self.correct_fixed = []
        self.incorrect_fixed = []
        self.generations = []
        self.learning_bits = []
        self.k=k

    def algo(self, i):
        # self.calc_fitness()  # evaluate all individuals in population
        self.local_search(1000)
        self.propablities_rank_based()
        self.evolve(i)  # evolve a new population
        self.population, self.buffer = self.buffer, self.population  # // swap buffers
        self.population = sorted(self.population)
        cf, icf, learning_bits = self.correctness()
        # for graphs
        self.correct_fixed.append(cf)
        self.incorrect_fixed.append(icf)
        self.learning_bits.append(learning_bits)
        self.generations.append(i)
        print("correctly fixed:", cf, " incorrectly fixed:", icf, " learning_bits:", learning_bits)
        self.solution = self.population[0]

    def stopage(self, i):
        k = i == 1000
        other_condition = self.learning_bits[i] == 0 and self.incorrect_fixed[i] <= 0.04
        if k or other_condition:
            plot(self.correct_fixed, self.incorrect_fixed, self.learning_bits, self.generations)
        return k or other_condition

    def evolve(self, i):
        GA_LAB1.mate(self, i) if not self.k else self.k_gene_exchange(i,self.k)

    def k_gene_exchange(self, gen,k):
        esize = self.serviving_genes(gen)
        # cross function for intial GA algo
        self.cross(esize, gen, self.population, k)

    def baldwin(self, individual):
        for index, i in enumerate(individual.object):
            if individual.object[index] == '?':
                individual.object[index] = individual.character_creation()

    def correctness(self):
        correctly_fixed = numpy.array([None] * self.pop_size)
        incorrectly_fixed = numpy.array([None] * self.pop_size)
        learnt_bits = numpy.array([None] * self.pop_size)
        for index, pop in enumerate(self.population):
            correct, incorrect = pop.fitnesstype['fixed'](pop.object, self.target)
            learnt_bits_num = self.target_size - correct - incorrect
            correctly_fixed[index], incorrectly_fixed[index] = correct, incorrect
            learnt_bits[index] = learnt_bits_num
        return correctly_fixed.mean() / self.target_size, incorrectly_fixed.mean() / self.target_size, learnt_bits.mean() / self.target_size

    def local_search(self, num_tries):
        tries = 0
        for index, pop in enumerate(self.population):
            for n in range(1, num_tries + 1):
                temp = self.prob_spec()
                # copy string
                temp.object = [i for i in pop.object]
                self.baldwin(temp)
                # check distance from target
                temp.calculate_fittness(self.target, self.target_size, 0, self.selection)
                # if distance is zero then calculate7 n (here we call it tries as in tries left) and send it to fitness function given in lecture
                if not temp.fitness:
                    self.population[index] = temp
                    del pop
                    tries = num_tries - n
                    break
            # fitness given in lecture : 1+(19+....)  explained in "baldwin" in fitness class
            self.population[index].fitnesstype['baldwin'](self.pop_size, tries, num_tries)

    # def lem_bald_learning(self, sub_population, type_of_learning):
    #     return self.baldwin(sub_population) if type_of_learning else self.lemarckian()
    # def lemarckian(self, sub_population):
    #     pass
    # def select_improve(self):
    #     # todo: select subset of individuals put them in selected
    #     selected = self.selection()
    #     # todo: individual improvment
    #     # todo: perform learning using memes for every individual in selected
    #     self.learning(selected)
    #     # todo: continue with Lemarkian or Baldwin learning
    #     self.lem_bald_learning(selected)
    #


class HybridMA(PureMA):
    def __init__(self, target, tar_size, pop_size, problem_spec, crosstype, fitnesstype, selection,
                 serviving_mechanizem, mutation, gene_dist, frequency, intensity,learning_algo,learning_fitness, mutation_probability=0):
        PureMA.__init__(self, target, tar_size, pop_size, problem_spec, crosstype, fitnesstype, selection,
                        serviving_mechanizem, mutation, gene_dist, 0)
        self.intensity=intensity
        self.frequency=frequency
        self.select_learning_alg={1:self.hill_climbing,2:self.random_walk,3:self.steapest_ascent}
        self.learning_algo=learning_algo
        self.learning_fitness=learning_fitness
        # selection parameter in previous classes is used for understanding which individuals will learn
    def search(self):
        pass
    def algo(self, i):
        self.calc_fitness()  # evaluate all individuals in population
        self.population = sorted(self.population)
        self.search()
        self.propablities_rank_based()
        self.evolve(i)  # evolve a new population
        self.population, self.buffer = self.buffer, self.population  # // swap buffers
        self.population = sorted(self.population)
        cf, icf, learning_bits = self.correctness()
        # for graphs
        self.correct_fixed.append(cf)
        self.incorrect_fixed.append(icf)
        self.learning_bits.append(learning_bits)
        self.generations.append(i)
        print("correctly fixed:", cf, " incorrectly fixed:", icf, " learning_bits:", learning_bits)
        self.solution = self.population[0]

    def random_walk(self, pop_size, hill_prabability):
        prob = [hill_prabability, 1 - hill_prabability]
        pos = [2]
        random_array = numpy.random.random(self.target_size)
        # create arrays of random places
        down = random_array < prob[0]
        up = random_array >= prob[1]
        for i, j in zip(up, down):
            down2 = j and pos[-1] > 1
            up2 = i and pos[-1] < self.target_size
            pos.append(pos[-1] - down2 + up2)
        # pos is an index array of random walk (positions to walk to )
        for i,citizen in enumerate(self.population):
            tries=0
            best=self.neighbours_given_pos(pos,citizen)
            while best.learning_fitness != 0 and self.intensity - tries > 0:
                best = self.best_neighbour(best)
            self.population[i] = best

    def neighbours_given_pos(self,pos,citizen):
        neighbours = []
        for i in pos:
            # get the member
            for j in pos:
                if j != i:
                    neighbour = citizen.copy()
                    neighbour.object[i] = citizen.object[j]
                    neighbour.object[j] = citizen.object[i]
                    neighbour.learning_fitness = neighbour.Learning_fitness(self.target, self.target_size,
                                                                            self.learning_fitness)
                    neighbours.append(neighbour)
        neighbours = sorted(neighbours)
        return neighbours[0]
    def local_search_of_individual(self, index, pop):
        tries = 0
        for n in range(1, self.intensity + 1):
            temp = self.prob_spec()
            # copy string
            temp.object = [i for i in pop.object]
            self.baldwin(temp)
            # check distance from target
            temp.calculate_fittness(self.target, self.target_size, 0, self.selection)
            # if distance is zero then calculate7 n (here we call it tries as in tries left) and send it to fitness function given in lecture
            if not temp.fitness:
                self.population[index] = temp
                del pop
                tries = self.intensity - n
                break
        # fitness given in lecture : 1+(19+....)  explained in "baldwin" in fitness class
        self.population[index].fitnesstype['baldwin'](self.pop_size, tries, self.intensity)

    def hill_climbing(self, pop_size, hill_probability=None):
        for i,pop in enumerate(self.population):
            tries = 0
            best_neighbour=self.best_neighbour(pop)
            while best_neighbour.learning_fitness!=0 and self.intensity-tries>0:
                best_neighbour=self.best_neighbour(best_neighbour)
            self.population[i]=best_neighbour
    def best_neighbour(self,citizen):
        neighbours=[]
        for i in range(len(citizen)):
            for j in range(i + 1, len(citizen)):
                neighbour = citizen.copy()
                neighbour.object[i] = citizen.object[j]
                neighbour.object[j] = citizen.object[i]
                neighbour.learning_fitness=neighbour.Learning_fitness(self.target, self.target_size, self.learning_fitness)
                neighbours.append(neighbour)
        neighbours=sorted(neighbours,key=lambda x:x.learning_fitness)
        return neighbours[0]
    def steapest_ascent(self,pop_size,hill_probability=None):
        pass
