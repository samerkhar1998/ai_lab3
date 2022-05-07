import matplotlib.pyplot as plt
from Genetic import GA_LAB1
from ACO import ACO_alg
from PSO import PSO_alg
import math
from simulated_annealing import simulated_annealing
from tabu_search import tabu
from create_problem_sets import nearest_neighbour,clark_wright
from settings import *
import time
# algo = {GenA: GA_LAB1, ISLAND: PureMA, ACO_PAR: ACO, SA: simulated_anealling, TS: Tabu_search, CO_PS: CO_PSO}
algo = {GenA: GA_LAB1, 2: ACO_alg,3:simulated_annealing,4:tabu }
tags = {1: "GA_CX_SWAP", 2: "ACO",3:"simulated_annealing",4:"tabu" }
heuristics={1: "NN", 2: "C&W"}
mutation_index={2:"SWAP",3:"INSERT"}
problem_sets_GA = {1: nearest_neighbour, 2: clark_wright}
# problem_sets_PSO = {BUL_PGIA: PSO_prb}
inputs_for_testing=["E-n22-k4", "E-n33-k4","E-n51-k5",  "E-n76-k8",  "E-n76-k10",
           "E-n101-k8",  "E-n101-k14"]
def plot(fitness, iter,tag,names):

    for i in range(len(fitness)):
        plt.plot(iter[i],fitness[i], label=names[i])
    plt.ylabel('fitness')
    plt.xlabel('iterations')
    plt.title(inputs_for_testing[tag])
    plt.legend()
    plt.show()



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


def ga_script():
    GA_POPSIZE=300
    max_iter=80
    for select_input in range(1,len(inputs.keys())+1):
        fitness_arr,iter_array=[],[]

        # generators

        # mutation
        Gene_dist = 4
        cities, cost_matrix, dimentions, capacity = get_sets_from_files(inputs[select_input])
        GA_TARGET = [cities, cost_matrix, dimentions, capacity]
        target_size = len(cities)
        names=[]
        for select_generator in range(1,3):
            problem_set = problem_sets_GA[select_generator]
            for mutation in range(2,4):

                print("GA_I_"+heuristics[select_generator]+"_"+mutation_index[mutation])

                sol=GA_LAB1(GA_TARGET, target_size, GA_POPSIZE, problem_set, CX_, "fitness", 3,
                                          1, mutation, Gene_dist,max_iter=max_iter)
                fitness,iteration=sol.solve()
                fitness_arr.append(fitness)
                iter_array.append(iteration)
                names.append("GA_I_"+heuristics[select_generator]+"_"+mutation_index[mutation])

                print("SA_"+heuristics[select_generator]+"_"+mutation_index[mutation])

                sol = algo[3](GA_TARGET, target_size, GA_POPSIZE, problem_set, "fitness", max_iter, mutation)
                fitness, iteration = sol.solve()
                fitness_arr.append(fitness)
                iter_array.append(iteration)
                names.append("SA_"+heuristics[select_generator]+"_"+mutation_index[mutation])

                print("TS_"+heuristics[select_generator]+"_"+mutation_index[mutation])

                sol = algo[4](GA_TARGET, target_size, GA_POPSIZE, problem_set, "fitness", max_iter, mutation)
                fitness, iteration = sol.solve()
                fitness_arr.append(fitness)
                iter_array.append(iteration)
                names.append("TS_"+heuristics[select_generator]+"_"+mutation_index[mutation])

            print("ACO_" + heuristics[select_generator] )

            sol = algo[2](GA_TARGET, target_size, GA_POPSIZE, problem_set, "fitness", max_iter)
            fitness, iteration = sol.solve()
            fitness_arr.append(fitness)
            iter_array.append(iteration)
            names.append("ACO_" + heuristics[select_generator] )

        plot(fitness_arr, iter_array, select_input,names)


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
        alg = int(input("chose algorithem :\n1:Island GA \n2: Ant Colony Optimization \n3: simulated annealing\n4: tabu search"))

        # solution = GA_LAB1(GA_TARGET, target_size, GA_POPSIZE, problem_set, crosstype, "fitness", 3,
        #                      serviving_stratigy, mutation, Gene_dist,max_iter=max_iter)
        solution = algo[alg](GA_TARGET, target_size, GA_POPSIZE, problem_set,"fitness",max_iter,mutation)

        overall_time = time.perf_counter()
        solution.solve()
        overall_time = time.perf_counter() - overall_time
        print(solution.max_iter)
        print("Overall runtime :", overall_time)

        print("\n run again ? press y for yes n for no ")
        if input() == "n":
            process = False


if __name__ == "__main__":
    ga_script()
