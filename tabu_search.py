from algorithems import algortithem

tabuMaxSize = 50
neighborhoodSize = 25


class tabu(algortithem):
    def _init_(self, target, tar_size, pop_size, problem_spec, fitnessType, max_iter, selection=None):
        algortithem._init_(self, target, tar_size, pop_size, problem_spec, fitnessType, selection, max_iter)
        self.cities = target[0]
        self.cost_matrix = target[1]
        self.dimensions = target[2]
        self.capacity = target[3]

        self.currSol = problem_spec()

        self.writ = ""
        self.sbest = problem_spec()
        self.sbest = self.sbest.create_object(self.target_size, self.target)

        self.sbest.create_object(self.target_size, self.target)
        self.bestCandidate = self.sbest
        self.tabuList = []
        self.tabuList.append(self.sbest)

    def getNeighbors(self, s):
        neighborhood = []
        for n in range(neighborhoodSize):
            # todo: hellp weith mutation
            # neighborhood.append(mutation(s))   # halllooooooooo ###############################
            continue
        return neighborhood

    def fitness(self, obj):
        fitness = self.prob_spec()
        fitness.object = obj
        return fitness.calculate_fittness(self.target, self.target_size, "fitness")

    def algo(self, i):

        # generate neighbors and take the fittest candidatee
        neighborhood = self.getNeighbors(self.bestCandidate)
        bestCandidate = neighborhood[0]
        for candidate in neighborhood:

            if candidate not in self.tabuList and self.fitness(candidate) < self.fitness(bestCandidate):
                bestCandidate = candidate
        if self.fitness(bestCandidate) < self.fitness(self.sbest):
            # tabulist = last best candidate
            sbest = bestCandidate
            self.tabuList.append(bestCandidate)

        # print("Iteration: ", i, " | Fitness: ", self.fitness(self.sbest))

        if len(self.tabuList) > tabuMaxSize:
            self.tabuList.remove(self.tabuList[0])

        self.solution.object = self.sbest
        self.solution.calculate_fitness(self.target, self.target_size, "fitness")