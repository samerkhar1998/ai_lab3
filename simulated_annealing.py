import math
import random

from algorithems import algortithem


class simulated_annealing(algortithem):
    def _init_(self, target, tar_size, pop_size, problem_spec, fitnessType, max_iter, selection=None):
        algortithem._init_(self, target, tar_size, pop_size, problem_spec, fitnessType, selection, max_iter)

        self.s = problem_spec()
        self.s = self.s.create_object(self.target_size, self.target)
        self.t = float(100)
        self.alpha = 0.3
        self.global_best = self.s

    def fitness(self, obj):
        fitness = self.prob_spec()
        fitness.object = obj
        return fitness.calculate_fittness(self.target, self.target_size, "fitness")

    def algo(self, i):

        # neighborhood = getNeighbors(s)
        # todo : help with mutation
        # sNew = swap_mutation(self.s)  # looooooooooooook heeeeeeeeeeerrrrrrrreeeeeeeeeeeeeeeeee #####################
        de = self.fitness(self.s) - self.fitness(sNew)
        temp = random.random()
        if de > 0 or math.exp(float(de) / 1.38 * float(self.t + 0.000001)) > temp:
            s = sNew
        self.t = float(self.t * self.alpha)
        if self.fitness(s) < self.fitness(self.global_best):
            global_best = s


        self.solution.object = self.global_best
        self.solution.calculate_fitness(self.target, self.target_size, "fitness")