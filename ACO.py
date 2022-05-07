from algorithems import algortithem
import numpy
from fitness_functions import fitness_selector

class ACO_alg(algortithem):
    def __init__(self, target, tar_size, pop_size, problem_spec, fitnesstype,max_iter, selection=None):
        algortithem.__init__(self, target, tar_size, pop_size, problem_spec, fitnesstype, selection,max_iter)
        self.cities = target[0]
        self.cost_matrix = target[1]
        self.dimentions = target[2]
        self.capacity = target[3]
        self.PheromoneMatrix,self.temp=self.initiate_phermones()
        self.global_sol = []
        self.current_sol =[]
        self.glob_counter = 0
        self.glob_visit = []
        self.distance=fitness_selector().city_dist

    def fitness(self, obj):
        fitness = self.prob_spec()
        fitness.object = obj
        return fitness.calculate_fittness(self.target, self.target_size, "fitness")
    def algo(self, i):
        cities=self.cities
        if self.glob_counter == round(self.max_iter / 16):
            self.PheromoneMatrix, self.temp = self.initiate_phermones()
            self.glob_counter = 0
            self.current_sol =[]

        visited = self.visited_cities(cities)
        dist = self.sum_of_distances(visited)

        self.PheromoneMatrix = self.updatePheromone(self.PheromoneMatrix, visited, dist)
        if len(self.current_sol) == 0 or len(self.global_sol ) == 0 or self.fitness(self.current_sol) > self.fitness(visited):
            self.current_sol = visited
            if len(self.global_sol ) == 0:
                self.global_sol = visited

        if self.fitness(self.current_sol) < self.fitness(self.global_sol ):
            self.glob_counter = 0
            self.global_sol  = self.current_sol
            self.glob_visit.append(self.global_sol )
        else:
            self.glob_counter += 1


        if self.fitness(self.current_sol)<self.fitness(self.global_sol):
            self.glob_counter = 0
            self.global_sol = self.current_sol
            self.glob_visit.append(self.global_sol)
        else:
            self.glob_counter += 1

        self.solution.object=self.global_sol
        self.solution.calculate_fittness(self.target, self.target_size, "fitness")

    def visited_cities(self, cities):
        visited = []
        while len(visited) != len(cities) - 1:
            if len(visited) != 0:
                self.temp = self.probabilities_of_visited(self.PheromoneMatrix, visited)
                self.temp[0] = 0
            sum_temp = sum(self.temp)
            self.temp = [float(self.temp[i] / sum_temp) for i in range(len(self.temp))]
            sol = numpy.random.choice(cities, p=self.temp)
            visited.append(sol.id)
        return visited

    def initiate_phermones(self):
        cities=self.cities
        PheromoneMatrix = [[1000 for i in range(len(cities))] for j in range(len(cities))]
        temp = [float(1 / (len(cities) - 1)) for _ in range(len(cities))]
        temp[0] = 0
        for i in range(len(cities)):
            j = 0
            PheromoneMatrix[i][j] = 0
            PheromoneMatrix[j][i] = 0
            PheromoneMatrix[i][i] = 0
        return PheromoneMatrix, temp


    def probabilities_of_visited(self,matrix, visited):
        cities = self.cities
        alpha = 4
        beta = 3
        phermos = [0 for _ in range(len(cities))]
        denominator = 0

        for i in range(len(cities)):  # i -> [1 to 22], visited[2 to 22], cities index [0 to 21]
            if i + 1 not in visited:
                tau = matrix[visited[len(visited) - 1] - 1][cities[i].id - 1]
                dist = self.distance(cities[visited[len(visited) - 1] - 1], cities[i])
                numerator = float(pow(tau, alpha)) * float(pow(float(1 / dist), beta))
                phermos[cities[i].id - 1] += numerator
                denominator += numerator
        for num in range(len(phermos)):
            phermos[num] += float(phermos[num] / denominator)
        return phermos

    def sum_of_distances(self,cities_dist):
        dist = 0
        for i in range(len(cities_dist) - 1):
            dist += self.distance(self.cities[cities_dist[i] - 1], self.cities[cities_dist[(i + 1)] - 1])
        return dist

    def updatePheromone(self,matrix, visited, pathLen):
        cities=self.cities
        rho = 0.1  # The trail persistence or evaporation rate
        for i in range(len(cities)):
            for j in range(len(cities)):
                matrix[i][j] = float(matrix[i][j] * (1 - rho))
        for i in range(len(visited) - 1):  # i -> [0 to 21]
            tau = matrix[visited[i] - 1][visited[(i + 1)] - 1]
            tau += float(rho * (float(100000 / pathLen)))
            matrix[visited[i] - 1][visited[(i + 1)] - 1] = tau
            matrix[visited[(i + 1)] - 1][visited[i] - 1] = tau

        return matrix

    def stopage(self, i):
        return False
