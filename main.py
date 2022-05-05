from settings import *
from Genetic import genetic_algorithem
from Speciation import Genetic_speciation
from PSO import PSO_alg
from Minimal_conflicts import Minimal_conflicts
from first_fit import FirstFit
from create_problem_sets import *
from MA import PureMA
import time


algo = {GenA: genetic_algorithem, ISLAND: PureMA, ACO_PAR: ACO, SA: simulated_anealling, TS: Tabu_search, CO_PS: CO_PSO}

problem_sets_GA = {NN: nearest_neighbour, CW: clark_write}
problem_sets_PSO = {BUL_PGIA: PSO_prb}

# todo : new problem sets


# todo : function to get files
inputs = {1: "E-n22-k4.txt", 2: "E-n33-k4.txt", 3: "E-n51-k5.txt", 4: "E-n76-k8.txt", 5: "E-n76-k10.txt",
          6: "E-n101-k8.txt", 7: "E-n101-k14.txt"}
dir = "./inputs/"

def get_sets_from_files(name):
    file = open(fr"inputs\{name}.txt", "r")
    weights = file.read().splitlines()
    weights1 = [int(k) for k in weights]
    file.close()


def get_bin_packing_weights(name):
    file = open(fr"inputs\{name}.txt", "r")
    weights = file.read().splitlines()
    weights1 = [int(k) for k in weights]
    file.close()

    return weights1[0], weights1[1], weights1[2:]

#todo: create cities so that we can use them initially , they will be sent to all algorithms
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
        serviving_stratigy = 1 # elite
        crosstype=3
        # pop size
        GA_POPSIZE = int(input("set population size:"))

        select_input = int(input("1: E-n22-k4.txt, 2: E-n33-k4.txt, 3: E-n51-k5.txt, 4: E-n76-k8.txt, 5: E-n76-k10.txt,"
                                 "6: E-n101-k8.txt, 7: E-n101-k14.txt"))
        # target ,from select_input
        #parameters= get_sets_from_files(inputs[select_input])
        GA_TARGET = None
        TAR_size = len(GA_TARGET)

        select_generator=int(input("select construction :  1:clark write  2:nearest neigbour"))
        # generators
        problem_set=problem_sets_GA[select_generator]
        # mutation
        mutation = int(
            input("choose mutation scheme:  random mutation: 1 ,swap_mutate: 2 ,insertion_mutate: 3"))
        # cho
        alg = int(input("chose algorithem :  1:GA  \n2:PSO 3:Minimal conflicts \n 4:first fit\n 5: baldwins\n 6:MA+GA"))
        solution = algo[alg](GA_TARGET, target_size, GA_POPSIZE, problem_set, crosstype, fit, selection,
                             serviving_stratigy, mutation, Gene_dist)

        overall_time = time.perf_counter()
        solution.solve()
        overall_time = time.perf_counter() - overall_time
        print("Overall runtime :", overall_time)

        print("\n run again ? press y for yes n for no ")
        if input() == "n":
            process = False


if __name__ == "__main__":
    main()
