import math
import random

from algorithems import algortithem
from mutations import mutations
neighborhoodSize = 25
class simulated_annealing(algortithem):
    def __init__(self, target, tar_size, pop_size, problem_spec, fitnessType, max_iter,mutation, selection=None):
        algortithem.__init__(self, target, tar_size, pop_size, problem_spec, fitnessType, selection, max_iter)
        self.mutation=mutations().select[mutation]
        self.s = problem_spec()
        self.s.create_object(self.target_size, self.target)
        self.s=self.s.object
        self.t = float(100)
        self.alpha = 0.3
        self.global_best = self.s

    def fitness(self, obj):
        fitness = self.prob_spec()
        fitness.object = obj
        return fitness.calculate_fittness(self.target, self.target_size, self.fitnesstype)
    def mutatate(self,s):
        snew=self.prob_spec()
        snew.object=s
        self.mutation(self.target_size, snew, self.prob_spec)
        return snew.object
    def getNeighbors(self, s):
        neighborhood = []
        for n in range(neighborhoodSize):
            neighborhood.append(self.mutatate(s))
        return neighborhood
    def get_best_Neighbour(self,neighborhood):
        N1=neighborhood[0]
        for N2 in neighborhood:
            N1=N2 if self.fitness(N2)<self.fitness(N1) else N1
        return N1
    def algo(self, i):

        neighborhood = self.getNeighbors(self.s)
        sNew = self.get_best_Neighbour(neighborhood)
        de = self.fitness(self.s) - self.fitness(sNew)
        temp = random.random()
        if de > 0 or math.exp(float(de) / 1.38 * float(self.t + 0.000001)) > temp:
            self.s = sNew
        self.t = float(self.t * self.alpha)
        if self.fitness(self.s) < self.fitness(self.global_best):
            self.global_best = self.s

        # update solution
        self.solution.object = self.global_best
        self.solution.calculate_fittness(self.target, self.target_size,self.fitnesstype)