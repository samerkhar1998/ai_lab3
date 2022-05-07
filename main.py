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
algo = {1: GA_LAB1, 2: ACO_alg,3:simulated_annealing,4:tabu }
tags = {1: "GA_CX_SWAP", 2: "ACO",3:"simulated_annealing",4:"tabu" }
heuristics={1: "NN", 2: "C&W"}
mutation_index={2:"SWAP",3:"INSERT"}
problem_sets_GA = {1: nearest_neighbour, 2: clark_wright}
# problem_sets_PSO = {BUL_PGIA: PSO_prb}
inputs_for_testing=["","E-n22-k4", "E-n33-k4","E-n51-k5",  "E-n76-k8",  "E-n76-k10",
           "E-n101-k8",  "E-n101-k14"]
def plot(fitness, iter,tag,names):

    for i in range(len(fitness)):
        plt.plot(iter[i],fitness[i], label=names[i])
    plt.ylabel('fitness')
    plt.xlabel('iterations')
    plt.title(inputs_for_testing[tag])
    plt.legend()
    plt.savefig(f"outputs\{inputs_for_testing[tag]}\{inputs_for_testing[tag]}-iter{len(iter[0])}.png")
    plt.close()


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
    file = open(fr"outputs\{name}\script_output.txt", "r")
    f = open(fr"outputs\Results.txt", "a")

    lines = file.readlines()
    lines = [x.split(' ') for x in lines]
    spaceforfirst=15
    fitnes=23
    all_lines=fitnes*3+spaceforfirst
    for _ in range(all_lines-2):f.write("-")
    mid=all_lines//2-len(name)//2
    f.write("\n")
    for _ in range(mid):f.write(" ")
    f.write(f"|{name}|")
    f.write("\n| Algorithem   |       fitness         |         Time          |      ticks      |\n")
    for _ in range(all_lines-2):f.write("-")
    for index,line in enumerate(lines):

        if str(line[0][:2])=="GA" or line[0][:2]=="TS" or line[0][:2]=="SA" or line[0][:2]=="AC":
            f.write("\n|")
            f.write(str(line[0][:len(line[0])-3]))
            for i in range(spaceforfirst-len(line[0])+2):
                f.write(" ")
            f.write("|")
        if len(line)>2 and len(line[2])>3:
            print(line)
            if str(line[1])==",fittness:":
                f.write(str(line[2]))
                for i in range(fitnes - len(line[2])):
                    f.write(" ")
                f.write("|")
        if len(line) > 3 and len(line[2]) > 3:
            if str(line[4]) == "Time":
                f.write(str(line[7]))
                for i in range(fitnes - len(line[7])):
                    f.write(" ")
                f.write("|")
        if len(line) > 8 and len(line[2]) > 3:
            if str(line[9]) == "ticks:":

                f.write(str(line[10][:len(line[10])-3]))
                for i in range(fitnes - len(line[10])-3):
                    f.write(" ")
                f.write("|\n")
                for _ in range(all_lines-2): f.write("-")



def ga_script(iterations,popsize):
    GA_POPSIZE=popsize
    max_iter=iterations
    Gene_dist = 4

    names = []
    select_generator = 1
    problem_set = problem_sets_GA[select_generator]

    for select_input in range(1,len(inputs.keys())+1):
        fitness_arr,iter_array=[],[]

        for select_generator in range(1, 3):
            cities, cost_matrix, dimentions, capacity = get_sets_from_files(inputs[select_input])
            GA_TARGET = [cities, cost_matrix, dimentions, capacity]
            target_size = len(cities)

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

def border():
    print("----------------------------------")
def main():

    process = True

    select_input = int(input("select data set:\n1: E-n22-k4.txt\n2: E-n33-k4.txt\n3: E-n51-k5.txt\n4: E-n76-k8.txt\n5: E-n76-k10.txt"
                             "\n6: E-n101-k8.txt\n7: E-n101-k14.txt"))
    border()
    while process:

        serviving_stratigy = 1  # elite
        crosstype = CX_
        mutation=1
        Gene_dist = 4
        GA_POPSIZE=1
        cities, cost_matrix, dimentions, capacity = get_sets_from_files(inputs[select_input])
        GA_TARGET = [cities, cost_matrix, dimentions, capacity]
        target_size = len(cities)

        # pop size
        border()

        alg = int(input("chose algorithem :\n1:Island GA \n2: Ant Colony Optimization \n3: simulated annealing\n4: tabu search"))
        border()

        max_iter = int(input("number of iterations:"))

        select_generator=int(input("select heuristic: \n1: nearest_neighbour \n2: clark_wright"))
        border()

        problem_set = problem_sets_GA[select_generator]
        if alg==1 or alg==4 or alg==3:
            border()

            mutation = int(input("select mutation:\n1: swap\n2: insert"))+1

        if alg==1:
            border()

            GA_POPSIZE = int(input("set population size:"))

            solution =GA_LAB1(GA_TARGET, target_size, GA_POPSIZE, problem_set, CX_, "fitness", 3,
                    1, mutation, Gene_dist, max_iter=max_iter)
        elif alg==3 or alg==4:
            solution = algo[alg](GA_TARGET, target_size, GA_POPSIZE, problem_set, "fitness", max_iter, mutation)
        else:
            solution = algo[2](GA_TARGET, target_size, GA_POPSIZE, problem_set, "fitness", max_iter)


        overall_time = time.perf_counter()
        solution.solve()
        overall_time = time.perf_counter() - overall_time
        border()
        print(solution.max_iter)
        print("Overall runtime :", overall_time)
        border()

        print("\n run again ? press y for yes n for no ")
        if input() == "n":
            process = False


if __name__ == "__main__":
    selector=int(input("select manual settings or test of all algorithms:\n1: manual  \n2:automatic test"))
    border()
    if selector==1:
        main()
    else:
        border()
        popsize = int(input("enter population size for all tests:"))
        border()
        iterations=int(input("enter  number of max iterations:"))
        ga_script(iterations,popsize)