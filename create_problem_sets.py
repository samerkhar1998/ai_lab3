import math
import random
import sys

import numpy
from numpy import unique, setdiff1d
from settings import PENALTY, HIGH_PENALTY, BIN
from fitness_functions import fitness_selector, hash_table
from mutations import mutations


# have to fill hash table with different keys when getting the command from main


# basic class for all problem sets because fittness and the member of the population are problem specific
# and we have to eliminate problem specifc parameters from the Genetic algorithem
# might add mutate !
class Agent:
    fitnesstype = fitness_selector().select

    def __init__(self):
        self.object = None
        self.learning_fitness=0
        self.algo_huristic=None
        self.age = 0
        self.fitness = 0

    # creates a member of the population
    def create_object(self, target_size, target):
        return self.object

    def character_creation(self, target_size):
        pass
    def Learning_fitness(self, target, target_size, huristic):
        self.learning_fitness = self.fitnesstype[huristic](self, target, target_size)
        return self.learning_fitness
    # function to calculate the fitness for this specific problem

    def calculate_fittness(self, target, target_size, select_fitness, age_update=True):
        self.fitness = self.fitnesstype[select_fitness](self, target, target_size)
        self.age += 1 if age_update else 0
        return self.fitness

    def create_special_parameter(self, target_size):
        pass

    # for sorting purposes
    def __lt__(self, other):
        return self.fitness < other.fitness

    def __str__(self):
        bstr = ""
        for i in self.object:
            bstr += str(i) + ","
        return bstr

    def __repr__(self):
        bstr = ""
        for i in self.object:
            bstr += str(i) + " "
        return bstr

    # def __eq__(self, other):
    #     self.fitness = other.fitness
    #     self.object = other.object
    # age !
    def hash(self, other):
        return self.object


# class for first problem
class DNA(Agent):
    mutation = mutations()

    def __init__(self):
        Agent.__init__(self)
        self.diversity = 0
        self.spiecy = 0

    def create_object(self, target_size, target):
        self.object = []
        for j in range(target_size):
            self.object += [self.character_creation(target_size)]
        self.create_special_parameter(target_size)
        return self.object

    def character_creation(self, target_size):
        return chr((random.randint(0, 90)) + 32)

    def mutate(self, target_size, member, mutation_type):
        self.mutation.select[mutation_type](target_size, member, self.character_creation)

    def hash(self, other):
        return ''.join(self.object + other.object)


# class for pso problem
class PSO_prb(DNA):
    # our object is the initial position , we added 2 parameters that are required
    def __init__(self):
        DNA.__init__(self)
        self.velocity = None
        self.p_best = sys.maxsize
        self.p_best_object = None

    def create_special_parameter(self, target_size):
        self.create_velocity(target_size)

    def create_velocity(self, target_size):
        self.velocity = [random.random() for i in range(target_size)]

    def calculate_new_position(self):
        pos = ""
        for i in range(len(self.object)):
            pos += chr((ord(self.object[i]) + int(self.velocity[i])) % 256)
        self.object = pos

    def calculate_velocity(self, c1, c2, gl_best, w=0.5):
        for i in range(len(self.object)):
            cc1 = c1 * (ord(self.p_best_object[i]) - ord(self.object[i])) * random.random()
            cc2 = c2 * (ord(gl_best[i]) - ord(self.object[i])) * random.random()
            self.velocity[i] = self.velocity[i] * w + cc1 + cc2

    def __eq__(self, other):
        DNA.__eq__(self, other)
        self.velocity = other.velocity
        self.best_object = other.best_object

    def __str__(self):
        if self.object == None:
            return ""
        else:
            return super(PSO_prb, self).__str__()

# todo: create new problem set for clark write
class clark_write(DNA):
    def __init__(self):
        super(clark_write, self).__init__()
    def create_object(self, target_size, target):
        #todo : self.object=result  , should be array of numbers/characters
        # cw_generator
        pass


class nearest_neighbour(DNA):
    def __init__(self):
        super(nearest_neighbour, self).__init__()

    def create_object(self, target_size, target):
        # todo : self.object=result  , nn_generator
        pass

