
import random
import sys
from fitness_functions import fitness_selector
from mutations import mutations
# have to fill hash table with different keys when getting the command from main


# basic class for all problem sets because fittness and the member of the population are problem specific
# and we have to eliminate problem specifc parameters from the Genetic algorithem
# might add mutate !
class Agent:
    fitnesstype = fitness_selector().select

    def __init__(self):
        self.object =[]
        self.learning_fitness=0
        self.algo_huristic=None
        self.age = 0
        self.fitness = 0
        self.solution=""

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
        bstr+=self.solution
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
class clark_wright(DNA):
    def __init__(self):
        super(clark_wright, self).__init__()
    def create_object(self, target_size, target):
        cities, cost_matrix, dimentions, capacity=target[0],target[1],target[2],target[3]
        tours = [[0, i, 0] for i in range(1, dimentions)]

        indexes, savings=self.savings(dimentions,cost_matrix)
        for i, j in indexes:
            # if len(tours) == num_vehicles:
            #     break
            for tour1 in tours:
                for tour2 in tours:
                    if tour1 != tour2:
                        demand1 = self.tourDemand(tour1,cities)
                        demand2 = self.tourDemand(tour2,cities)
                        if demand1 + demand2 > capacity:
                            continue

                        new_tour = []
                        if tour1[-2] == i and tour2[1] == j:
                            new_tour = tour1[:len(tour1) - 1] + tour2[1:]
                        if tour1[1] == i and tour2[-2] == j:
                            new_tour = tour2[:len(tour2) - 1] + tour1[1:]
                        if len(new_tour):
                            tours.remove(tour1)
                            tours.remove(tour2)
                            tours.append(new_tour)
                            break
        final_tour = []
        for tour in tours:
            final_tour += tour[1:len(tour) - 1]

        ret = []
        for t in final_tour:
            ret.append(t + 1)
        self.object=ret

    def tourDemand(self,tour,cities):
        sum = 0
        for city in tour:
            sum += cities[city].demand
        return sum

    def savings(self,dimentions,cost_matrix):
        # savings for (i, j) = cost(i,0) + cost(0,j) - cost(i,j)
        # returns list of savings for all city pairs (i, j)
        savings = {}
        for i in range(1, dimentions - 1):
            for j in range(i + 1, dimentions):
                saved = cost_matrix[0][i] + cost_matrix[0][j] - cost_matrix[i][j]
                savings[(i, j)] = saved

        sorted_indexes = sorted(savings, key=savings.get, reverse=True)
        return sorted_indexes, savings

class nearest_neighbour(DNA):
    def __init__(self):
        super(nearest_neighbour, self).__init__()
    def create_object(self, target_size, target):
        cities, cost_matrix, dimentions, capacity = target[0], target[1], target[2], target[3]
        available = [i for i in range(1, len(cities))]
        arr = []
        city = random.choice(cities[1:])
        id = city.id - 1
        arr.append(id + 1)
        available.remove(id)
        for i in range(len(cities) - 2):
            mini = city.neighb[available[0]]
            index = available[0]
            for j in available:
                if city.neighb[j] < mini:
                    index = j
                    mini = city.neighb[j]
            available.remove(index)
            arr.append(index + 1)
        self.object=arr

