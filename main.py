
from Genetic import GA_LAB1
import math

from create_problem_sets import nearest_neighbour,clark_wright
from settings import *
import time

# algo = {GenA: genetic_algorithem, ISLAND: PureMA, ACO_PAR: ACO, SA: simulated_anealling, TS: Tabu_search, CO_PS: CO_PSO}

problem_sets_GA = {1: nearest_neighbour, 2: clark_wright}
# problem_sets_PSO = {BUL_PGIA: PSO_prb}





inputs = {1: "E-n22-k4.txt", 2: "E-n33-k4.txt", 3: "E-n51-k5.txt", 4: "E-n76-k8.txt", 5: "E-n76-k10.txt",
          6: "E-n101-k8.txt", 7: "E-n101-k14.txt"}
dir = "./inputs/"


class City:
    def __init__(self, id, x, y, dimension):
        self.id = id
        self.demand = 0
        self.x, self.y = x, y
        self.neighb = [0] * dimension

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        return distance


def get_sets_from_files(name):
    global cities, cost_matrix, dimentions, capacity
    file = open(fr"inputs\{name}", "r")
    lines = file.readlines()
    lines = [x.split(' ') for x in lines]
    dimentions = int(lines[3][2])
    capacity = int(lines[5][2])
    cities = []
    cost_matrix = [[0 for i in range(dimentions)] for j in range(dimentions)]
    for i in lines[7: dimentions + 7]:
        i[2] = i[2].rstrip("\n")
        city = City(int(i[0]), int(i[1]), int(i[2]), dimentions)
        if len(cities):
            for c in cities:
                dist = city.distance(c)
                c.neighb[city.id - 1] = dist
                city.neighb[c.id - 1] = dist
        cities.append(city)

    for i in lines[dimentions + 8: dimentions + dimentions + 8]:
        if len(cities):
            if len(cities) + 1 > int(i[0]) - 1 > 0:
                i[1] = i[1].rstrip("\n")
                cities[int(i[0]) - 1].demand = int(i[1])

    for i in range(dimentions):
        for j in range(dimentions):
            cost_matrix[i][j] = cities[i].neighb[j]

    return cities, cost_matrix, dimentions, capacity


# todo: create cities so that we can use them initially , they will be sent to all algorithms
# todo: flow is :
#  1. create cities class.
#  2. get cities from input
#  3. send them either to algorithm or fitness function
#  3.1.  create data sets,so that the algorithms understand the data
#  3.2.  check correctness of generated data
#  3.3.  understand how to translate the data to cities and cars (i.e fitness function)
#  4. solve problem for GA
#  5. solve for the rest of algorithms

def main():

    process = True
    Gene_dist = 4
    GA_TARGET = None
    while process:
        '''
        get input
        pop size
        select input 
        generators 
        mutation
        algo 
        '''
        # get_sets_from_files(name)
        # default vals
        serviving_stratigy = 1  # elite
        crosstype = CX_
        # pop size
        GA_POPSIZE = int(input("set population size:"))
        max_iter=int(input("number of iterations:"))
        print("max",max_iter)
        select_input = int(input("1: E-n22-k4.txt, 2: E-n33-k4.txt, 3: E-n51-k5.txt, 4: E-n76-k8.txt, 5: E-n76-k10.txt,"
                                 "6: E-n101-k8.txt, 7: E-n101-k14.txt"))
        # target ,from select_input
        cities, cost_matrix, dimentions, capacity = get_sets_from_files(inputs[select_input])
        GA_TARGET = [cities, cost_matrix, dimentions, capacity]
        target_size = len(cities)

        select_generator = int(input("select construction :  1:clark write  2:nearest neigbour"))
        # generators
        problem_set = problem_sets_GA[select_generator]
        # mutation
        mutation = int(
            input("choose mutation scheme:  random mutation: 1 ,swap_mutate: 2 ,insertion_mutate: 3"))
        # cho
        alg = int(input("chose algorithem :\n  1:GA "))

        solution = GA_LAB1(GA_TARGET, target_size, GA_POPSIZE, problem_set, crosstype, "fitness", 3,
                             serviving_stratigy, mutation, Gene_dist,max_iter=max_iter)
        # solution = algo[alg](GA_TARGET, target_size, GA_POPSIZE, problem_set, crosstype, "fitness", 3,
        #                      serviving_stratigy, mutation, Gene_dist)

        overall_time = time.perf_counter()
        solution.solve()
        overall_time = time.perf_counter() - overall_time
        print(solution.max_iter)
        print("Overall runtime :", overall_time)

        print("\n run again ? press y for yes n for no ")
        if input() == "n":
            process = False


if __name__ == "__main__":
    main()
