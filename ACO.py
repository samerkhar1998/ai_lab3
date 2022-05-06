from algorithems import algortithem
import numpy
from fitness_functions import fitness_selector

class ACO_alg(algortithem):
    def __init__(self, target, tar_size, pop_size, problem_spec, fitnesstype,max_iter, selection=None):
        algortithem.__init__(self, target, tar_size, pop_size, problem_spec, fitnesstype, selection,max_iter)
        self.global_minima = problem_spec()
        self.local_minima = problem_spec()
        self.cities = target[0]
        self.cost_matrix = target[1]
        self.dimentions = target[2]
        self.capacity = target[3]
        self.phermones,self.probablities=self.initiate_phermones()
        self.global_sol = problem_spec()
        self.current_sol =problem_spec()
        self.glob_counter = 0
        self.glob_visit = problem_spec()
        self.distance=fitness_selector().city_dist
        self.fitness=fitness_selector().fitness
    def algo(self, i):
        if  self.glob_counter == round(self.max_iter / 16):
            self.initiate_phermones()
            self.glob_counter = 0
            self.current_sol.object = []
        visited=self.get_visited_cities()
        vis=self.prob_spec()
        vis.object=visited
        dist=self.sum_of_distances(visited)
        self.updatePheromone(visited,dist)
        self.current_sol.calculate_fittness(self.target, self.target_size,"fitness")
        vis.calculate_fittness(self.target, self.target_size,"fitness")
        if len(self.current_sol.object) == 0 or len(self.global_sol.object) == 0 or\
                self.current_sol.fitness > vis.fitness:
            self.current_sol.object = visited
            if len(self.global_sol) == 0:
                self.global_sol.object = visited
        self.global_sol.calculate_fittness(self.target, self.target_size,"fitness")
        if self.current_sol.fitness<self.global_sol.fitness:
            self.glob_counter = 0
            self.global_sol.object = self.current_sol.object
            self.glob_visit.append(self.global_sol)
        else:
            self.glob_counter += 1

    def initiate_phermones(self):
        self.PheromoneMatrix = [[1000 for i in range(len(self.cities))] for j in range(len(self.cities))]
        self.probablities = [float(1 / (len(self.cities) - 1)) for _ in range(len(self.cities))]
        self.probablities[0] = 0
        for i in range(len(self.cities)):
            self.PheromoneMatrix[i][0] = self.PheromoneMatrix[0][i] = self.PheromoneMatrix[i][i] = 0
        return self.PheromoneMatrix, self.probablities

    def get_visited_cities(self):
        visited=[]
        while len(visited) != len(self.cities) - 1:
            if len(visited) != 0:
                self.probabilities(self.PheromoneMatrix, visited)
                self.probablities[0] = 0
            prob_sum=sum(self.probablities)
            self.probablities =[i/prob_sum for i in self.probablities]
            sol = numpy.random.choice(self.cities, p=self.probablities)
            visited.append(sol.id)
        return visited

    def probabilities(self,matrix, visited):
        alpha = 4
        beta = 3
        phermos = [0 for _ in range(len(self.cities))]
        denominator = 0

        for i in range(len(self.cities)):  # i -> [1 to 22], visited[2 to 22], cities index [0 to 21]
            if i + 1 not in visited:
                tau = matrix[visited[len(visited) - 1] - 1][self.cities[i].id - 1]
                dist = self.distance(self.cities[visited[len(visited) - 1] - 1], self.cities[i])
                numerator = float(pow(tau, alpha)) * float(pow(float(1 / dist), beta))
                phermos[self.cities[i].id - 1] += numerator
                denominator += numerator
        for num in range(len(phermos)):
            phermos[num] += float(phermos[num] / denominator)
        return phermos
    def sum_of_distances(self,cities_dist):
        dist = 0
        for i in range(len(cities_dist) - 1):
            dist += self.distance(self.cities[cities_dist[i] - 1], self.cities[cities_dist[(i + 1)] - 1])
        return dist

    def updatePheromone(self, visited, pathLen):
        trail_persistance = 0.1
        for i in range(len(self.cities)):
            for j in range(len(self.cities)):
                self.phermones[i][j] = float(self.phermones[i][j] * (1 - trail_persistance))
        for i in range(len(visited) - 1):  # i -> [0 to 21]
            tau = self.phermones[visited[i] - 1][visited[(i + 1)] - 1]
            tau += float(trail_persistance * (float(100000 / pathLen)))
            self.phermones[visited[i] - 1][visited[(i + 1)] - 1] = tau
            self.phermones[visited[(i + 1)] - 1][visited[i] - 1] = tau


    def stopage(self, i):
        return False
