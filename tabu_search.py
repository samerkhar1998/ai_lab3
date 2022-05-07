from algorithems import algortithem
from mutations import mutations
tabuMaxSize = 50
neighborhoodSize = 25
class tabu(algortithem):
    def __init__(self, target, tar_size, pop_size, problem_spec, fitnessType, max_iter,mutation, selection=None):
        algortithem.__init__(self, target, tar_size, pop_size, problem_spec, fitnessType, selection, max_iter)
        self.cities = target[0]
        self.cost_matrix = target[1]
        self.dimensions = target[2]
        self.capacity = target[3]

        self.mutation = mutations().select[mutation]
        self.sbest = problem_spec()
        self.sbest.create_object(self.target_size, self.target)
        self.sbest=self.sbest.object
        self.bestCandidate = self.sbest
        self.tabuList = []
        self.tabuList.append(self.sbest)

    def mutatate(self, s):
        snew = self.prob_spec()
        snew.object = s
        self.mutation(self.target_size, snew, self.prob_spec)
        return snew.object

    def getNeighbors(self, s):
        neighborhood = []
        for n in range(neighborhoodSize):
            snew=self.mutatate(s)
            neighborhood.append(snew)  # halllooooooooo ###############################
            continue
        return neighborhood

    def fitness(self, obj):
        fitness = self.prob_spec()
        fitness.object = obj
        return fitness.calculate_fittness(self.target, self.target_size, "fitness")

    def algo(self, i):

        # generate neighbors and take the fittest candidatee
        neighborhood = self.getNeighbors(self.bestCandidate)
        self.bestCandidate = neighborhood[0]
        for candidate in neighborhood:
            if candidate not in self.tabuList and self.fitness(candidate) < self.fitness(self.bestCandidate):
                self.bestCandidate = candidate
        if self.fitness(self.bestCandidate) < self.fitness(self.sbest):
            # tabulist = last best candidate
            self.sbest = self.bestCandidate
            self.tabuList.append(self.bestCandidate)

        if len(self.tabuList) > tabuMaxSize:
            self.tabuList.remove(self.tabuList[0])
        # update solution
        self.solution.object = self.sbest
        self.solution.calculate_fittness(self.target, self.target_size, "fitness")