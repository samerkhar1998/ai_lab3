import math
import time
from Selection_methods import selection_methods
from settings import GA_MAXITER

import numpy


class algortithem:
    def __init__(self, target, tar_size, pop_size, problem_spec, fitnesstype, selection,max_iter):
        self.population = list(range(pop_size))
        self.buffer = list(range(pop_size))
        self.fitness_array = numpy.zeros((pop_size))
        self.target = target
        self.target_size = tar_size
        self.pop_size = pop_size
        self.pop_mean = 0
        self.iteration = 0  # current iteration that went through the algorithem
        self.prob_spec = problem_spec
        self.file = open(r"pres.txt", "w+")
        self.file.close()
        self.fitnesstype = fitnesstype
        self.selection_methods = selection_methods()
        self.selection = selection
        self.tick = 0
        self.sol_time = 0
        self.max_iter=max_iter
        self.solution = problem_spec()


    def init_population(self):
        for i in range(self.pop_size):
            citizen = self.prob_spec()
            citizen.create_object(self.target_size,self.target)

            citizen.calculate_fittness(self.target, self.target_size, self.fitnesstype,self.selection)
            self.population[i] = self.buffer[i] = citizen
        # self.update_fitness_array()
        self.sort_by_fitness()

    def calc_fitness(self):
        mean = 0
        for i in range(self.pop_size):
            self.population[i].calculate_fittness(self.target, self.target_size, self.fitnesstype)
            mean += self.population[i].fitness
            # calculate diversity for each individual
        self.pop_mean = mean / self.pop_size

    def sort_by_fitness(self):
        self.population = sorted(self.population)




    def handle_initial_time(self):
        self.tick = time.time()
        self.sol_time = time.perf_counter()

    def handle_prints_time(self):
        runtime = time.perf_counter() - self.sol_time
        clockticks = time.time() - self.tick
        print_B(self.solution)
        # print_mean_var((self.pop_mean, variance((self.pop_mean, self.solution.fitness))))
        print_time((runtime, clockticks))

    def algo(self, i):
        pass

    def stopage(self,i):
        return self.population[0].fitness == 0

    def solve(self):
        self.handle_initial_time()
        self.init_population()
        for i in range(self.max_iter):

            self.iteration += 1
            self.algo(i)
            # self.handle_prints_time()
            if self.stopage(i) or i==self.max_iter-1:
                print(" number of generations : ",i)
                self.handle_prints_time()
                break


        return 0


# print_B = lambda x: print(f" Best:{len(x.object)} ,fittness: {x.fitness} ", end=" ")
print_B = lambda x: print(f" Best:{ x.solution } ,fittness: {x.fitness} ", end=" ")
# print_B = lambda x: print(f" Best: {x.object} ,fittness: {x.fitness} ", end=" ")

#  prints mean and variance
print_mean_var = lambda x: print(f"Mean: {x[0]} ,Variance: {x[1]}", end=" ")
# prints time
print_time = lambda x: print(f"Time :  {x[0]}  ticks: {x[1]}")
# calculates variance
variance = lambda x: math.sqrt((x[0] - x[1]) ** 2)
