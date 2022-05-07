from algorithems import *
from settings import GA_MAXITER,NQUEENS
from random import choice
def create_results_file(name):
    file = open(fr"outputs\{name}", "r")
    f = open(fr"newoutput\{name}", "w+")
    for _ in range(50):f.write("-")

    lines = file.readlines()
    lines = [x.split(' ') for x in lines]
    spaceforfirst=20
    for index,line in enumerate(lines):
        if line[:2]=="GA" or line[:2]=="TS" or line[:2]=="SA" or line[:2]=="AC":
            f.write("|")
            f.write(str(line))
            for i in range(len(line)-spaceforfirst):
                f.write(" ")
            f.write("|")
        if line[1:3]=="fi":
            f.write("|")
            f.write(str(lines[index+1]))
            f.write("|")
        if line[:3] == "Ti":
            f.write("|")
            f.write(str(lines[index + 1]))
            f.write("|")
        if line[:3] == "ti":
            f.write("|")
            f.write(str(lines[index + 1]))
            f.write("|")

class PSO_alg(algortithem):
    def __init__(self, target, tar_size, pop_size, problem_spec, fitnesstype,max_iter, selection=None):
        algortithem.__init__(self, target, tar_size, pop_size, problem_spec, fitnesstype, selection,max_iter)
        self.global_minima = problem_spec()
        self.local_minima = problem_spec()

    def calc_fitness(self):

        mean = 0
        for particle in self.population:

            particle.calculate_fittness(self.target, self.target_size, self.fitnesstype)

            if particle.fitness == 0:
                self.solution = self.global_minima = particle
                break
            if particle.fitness < self.global_minima.fitness:
                self.solution = self.global_minima = particle

            if particle.fitness < particle.p_best:
                particle.p_best = particle.fitness
                particle.p_best_object = particle.object

            mean += particle.fitness
        self.pop_mean = mean / self.pop_size

    def algo(self, i):
        if i == 0:
            self.global_minima.object = self.population[0].object
            self.global_minima.calculate_fittness(self.target, self.target_size, self.fitnesstype)
        self.calc_fitness()
        self.sort_by_fitness()
        w = ((i - GA_MAXITER) * 0.4) / (GA_MAXITER ** 2 + 0.4)
        c1 = ((-3 * i) / GA_MAXITER) + 3.5
        c2 = ((3 * i) / GA_MAXITER) + 0.5
        if not self.stopage(i):
            for particle in self.population:
                particle.calculate_velocity(self.target,c1, c2, self.global_minima.object, w)
                particle.calculate_new_position()

    def stopage(self,i):
        return self.global_minima.fitness == 0


