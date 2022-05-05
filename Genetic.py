import random

from function_selection import cross_types
from algorithems import algortithem
from settings import *
from sys import maxsize
import numpy
import math


""" to generalize the problem we created a class that given a population calculates the solution"""




def adaptive_decrease(p, rate, generation):
    return 2 * (p ** 2) * math.exp(rate * generation) / (p + p * math.exp(rate * generation))


class genetic_algorithem(algortithem):
    Distance_hash = {}

    def __init__(self, target, tar_size, pop_size, problem_spec, crosstype, fitnesstype, selection,
                 serviving_mechanizem, mutation, gene_dist, max_iter,mutation_probability=0):
        algortithem.__init__(self, target, tar_size, pop_size, problem_spec, fitnesstype, selection,max_iter)
        self.cross_func = cross_types().select[crosstype]
        self.serviving = serviving_mechanizem
        self.mutation_type = mutation
        self.gene_dist = self.prob_spec().fitnesstype[gene_dist]
        self.selection_pressure = self.pop_diversity = 0
        self.hyper_mutaion = mutation_probability
        self.trigger_mutation = False
        self.elite_rate=GA_ELITRATE

    # overload the calc_fitness function to also calculate diversity,
    # fitness calculation is done in mate() when creating new chromosomes we dont need it now !
    def calc_diversity(self):
        # if the distance is levishtine distance we can aproximate it by calculating the difference
        # between 2 strings on all the population
        # by that we mean the distance between all the population and one string
        # and then using a+b<c to approximate it !
        # Distance_hash = {}
        mean = 0
        self.pop_diversity = 0
        counter = 0
        counter2 = 0
        # print(len(self.population),"pop size")
        for i in range(self.pop_size):
            self.population[i].diversity = 0
            mean += self.population[i].fitness
            # for j in sample:
            for j in range(self.pop_size):
                # calculate diversity for each individual with a hash table so that we don't
                # calculate the same string twice
                strings = self.population[i].hash(self.population[j])
                strings2 = self.population[j].hash(self.population[i])
                if strings in self.Distance_hash.keys():
                    self.population[i].diversity += self.Distance_hash[strings]
                    counter += 1
                elif strings2 in self.Distance_hash.keys():
                    counter += 1
                    self.population[i].diversity += self.Distance_hash[strings2]
                else:
                    counter2 += 1
                    self.Distance_hash[strings] = self.gene_dist(self.population[i].object, self.population[j].object)
                    self.population[i].diversity += self.Distance_hash[strings]
            self.population[i].diversity = self.population[i].diversity / self.pop_size
            self.pop_diversity += self.population[i].diversity
            self.pop_mean = mean / self.pop_size

        # divide by all population to get population diversity
        # print("hashed",counter,"first time hash ",counter2)
        old_pop_diversity = self.pop_diversity
        self.pop_diversity /= self.pop_size

        self.trigger_mutation = True if old_pop_diversity < self.pop_diversity else False

    # this function assumes that the population is sorted by asscending order of the fitness value

    def propablities_rank_based(self):

        # depending on the selection scheme get propabilities from ranking system !
        multiplier = 1 if self.selection == SUS or RWS else 0.5  # for now keep it like this
        # scale fitness values with linear ranking for sus and RWS
        if self.selection == SUS:

            mio = self.pop_size
            self.fitness_array = numpy.array([p_linear_rank(mio, int(i)) for i in range(self.pop_size - 1, -1, -1)])
        # get accumulative sum of above values
        elif self.selection == RWS:
            mean = numpy.mean(self.fitness_array)
            std = numpy.std(self.fitness_array)
            # linear scale
            self.fitness_array = numpy.array([i for i in range((self.pop_size + 1) * 10, 10, -10)])
            # sigma scale
            self.fitness_array = numpy.array(
                [max((f - mean) / (2 * std), 1) if std > 0 else 1 for f in self.fitness_array])
            sum = self.fitness_array.sum()
            self.fitness_array = numpy.array([i / sum for i in self.fitness_array])

        else:
            # fps  for tournament selection
            self.fitness_array = numpy.array([pop.fitness for pop in self.population])
            sumof_fit = self.fitness_array.sum()
            sumof_fit = sumof_fit if sumof_fit else 1
            self.fitness_array = numpy.array([(pop.fitness + 1) / sumof_fit for pop in self.population])

        # selection pressure :
        self.selection_pressure = self.fitness_array[0] / numpy.mean(
            self.fitness_array) if self.fitness_array.any() else 0
        if self.selection_pressure and (self.selection != SUS and self.selection != RWS):
            self.selection_pressure = 1 / self.selection_pressure

    def mutate(self, member):
        member.mutate(self.target_size, member, self.mutation_type)
        member.calculate_fittness(self.target, self.target_size, self.fitnesstype)

    def age_based(self):
        age_based_population = [citizen for citizen in self.population if 2 <= citizen.age <= 20]
        self.buffer[:len(age_based_population)] = age_based_population[:]
        return len(age_based_population)

    # selection of the servivng mechanizem
    def serviving_genes(self,gen):
        # elitizem
        # elite_rate=GA_ELITRATE
        # self.elite_rate+=0.005 if self.elite_rate<0.75 else self.elite_rate
        # print(self.elite_rate)
        esize = math.floor(self.pop_size *self.elite_rate)
        if self.serviving == ELITIZEM:
            self.buffer[:esize] = self.population[:esize]
        # age
        elif self.serviving == AGE:
            esize = self.age_based()
        return esize

    # this function returns an array for each spiecy , how many are elite
    # so that we can choose the appropriate ammount of genes from speciy and so that the population size stayes the same

    def mate(self, gen):
        esize = self.serviving_genes(gen)
        # cross function for intial GA algo
        self.cross(esize, gen, self.population, self.pop_size - esize)

    def cross(self, esize, gen, population, birth_count):
        for i in range(esize, esize + birth_count):
            self.buffer[i] = self.prob_spec()
            citizen1 = self.prob_spec()
            citizen2 = self.prob_spec()
            # condition = True
            i1, i2 = self.selection_methods.method[self.selection](population, self.fitness_array)
            # counter+=1
            citizen1.object, citizen2.object = self.cross_func(i1, i2)
            citizen1.calculate_fittness(self.target, self.target_size, self.fitnesstype)
            citizen2.calculate_fittness(self.target, self.target_size, self.fitnesstype)

            # mutation
            mutation = GA_MUTATION if (
                        (not self.hyper_mutaion) and self.trigger_mutation) else maxsize * adaptive_decrease(0.75, 1,
                                                                                                             gen)
            if random.randint(0, maxsize) < mutation:
                self.mutate(citizen1)
                self.mutate(citizen2)

            # select best of the two
            self.buffer[i] = citizen1 if citizen1.fitness < citizen2.fitness else citizen2

    def algo(self, i):
        self.calc_diversity()  # calculate fitness
        self.sort_by_fitness()
        self.propablities_rank_based()
        self.mate(i)  # mate the population together
        self.population, self.buffer = self.buffer, self.population  # // swap buffers
        self.solution = self.population[0]

        print("\nselection pressure:", self.selection_pressure, "  Diversity: ", self.pop_diversity)

class GA_LAB1(genetic_algorithem):
    def __init__(self, target, tar_size, pop_size, problem_spec, crosstype, fitnesstype, selection,
                 serviving_mechanizem, mutation, gene_dist,max_iter, mutation_probability=0):
        genetic_algorithem.__init__(self, target, tar_size, pop_size, problem_spec, crosstype, fitnesstype, selection,
                 serviving_mechanizem, mutation, gene_dist,max_iter,mutation_probability)
    def algo(self, i):
        self.sort_by_fitness()
        self.propablities_rank_based()
        self.mate(i)  # mate the population together
        self.population, self.buffer = self.buffer, self.population  # // swap buffers
        self.solution = self.population[0]
# inline functions
linear_scale = lambda x: x[0] * x[1] + x[2]


# (s,mio,i)
def p_linear_rank(mio, i, s=1.5):
    if mio > 1:
        return (2 - s) / mio + 2 * i * (s - 1) / (mio * (mio - 1))
    else:
        return 1

# the general idea is to create 2 genetic algorithims one that works on a given population and given elite members
# the second one uses the first class to work on each spiecy and then adds the solutions together
