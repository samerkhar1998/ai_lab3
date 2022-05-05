# class for fitness functions , add your fitness function here !
import math
from settings import BIN, HIGH_PENALTY, PENALTY, LIV_DIST, KINDL_TAU
from numpy import unique
import numpy
hash_table = {}

# todo: fitness function that translate's input into cars+cities that returns a value
class fitness_selector:
    def __init__(self):
        self.select = {0: self.distance_fittness, 1: self.bul_pqia, 2: self.n_queens_conflict,
                       3: self.n_queens_conf_based_on_place, BIN: self.bins_fitness,
                       LIV_DIST: self.levenshteinDistance, KINDL_TAU: self.kendallTau, 'baldwin': self.baldwinss,
                       "fixed": self.fixed_distance,"fitness":self.fitness}

    def distance_fittness(self, object, target, target_size):
        fitness = 0
        for j in range(target_size):
            fit = ord(object.object[j]) - ord(target[j])
            fitness += abs(fit)
        return fitness

    def bul_pqia(self, object, target, target_size):
        fitness = 0
        for i in range(target_size):
            if ord(object.object[i]) != ord(target[i]):
                fitness += PENALTY if object.object[i] in target else HIGH_PENALTY
        return fitness

    # fitness for NQueens:
    def n_queens_conflict(self, object, target, target_size):
        conflicts = 0
        for col in range(target_size):
            for row in range(target_size):
                if row != col:
                    # check if more than one queen is on the same right diagonal "/"
                    conflicts += 1 if abs(row - col) == abs(object.object[col] - object.object[row]) else 0
        # check for duplicates ! ,cannot be detected by diagonal's
        conflicts += abs(len(unique(object.object)) - len(object.object))

        return conflicts

    def n_queens_conf_based_on_place(self, object, row, col):
        conflicts = 0
        for i in range(len(object.object)):
            if i == col:
                continue
            if (object.object[i] == row or abs(object.object[i] - row) == abs(i - col)):
                conflicts += 1
        return conflicts

    def bins_fitness(self, object, target, target_size):

        object.create_special_parameter(target_size)
        capacity = object.bin_objects[0].capacity
        sumof = sum([hash_table[i] for i in object.object]) / capacity

        number_of_bins = len(object.bin_objects)
        # return abs(ceil(sumof*9/8)-number_of_bins)
        return number_of_bins

    # these functions take [] as input , not a class instance !

    def levinshtine_distance(self, a, b, target_size=0):
        """ if one of them is of length 0 return the length of the other """
        if len(a) == 0:
            return len(b)
        elif len(b) == 0:
            return len(a)
        # if the first character matches then go farther in the strings
        elif a[0] == b[0]:
            return self.levinshtine_distance(a[1:], b[1:])
        # x calculate distance between the first string without the first character with the second string
        # y same as x but cuts down b by one( takes the tail of b with full a
        # z compares both tales of a and b
        else:
            x, y, z = self.levinshtine_distance(a[1:], b), self.levinshtine_distance(a,
                                                                                     b[1:]), self.levinshtine_distance(
                a[1:], b[1:])
            return 1 + min(x, y, z)

    # this function is based on dynamic programming that we learned in data structures
    # create a 2d matrix and add distances based on previous distances , the final value will be in distances[max][max]
    def levenshteinDistance(self, first, second, target_size=0):
        distances = numpy.zeros((len(first) + 1, len(second) + 1))
        # assighn 2 strings in the first column and first row
        for object in range(len(first) + 1):
            distances[object][0] = object
        for target in range(len(second) + 1):
            distances[0][target] = target
        # x,y,z=0,0,0
        # go over the object and the target and assign the values to the 2d array
        for object in range(1, len(first) + 1):
            for target in range(1, len(second) + 1):
                # if current 2 are the same string add the distance of the previous place in that distance matrix
                if first[object - 1] == second[target - 1]:
                    distances[object][target] = distances[object - 1][target - 1]
                else:
                    # if they are not then get 3 values of previous calculations and check them ,then place the appropriate value + 1 wich is the new non-matching character
                    x, y, z = distances[object][target - 1], distances[object - 1][target], distances[object - 1][
                        target - 1]
                    distances[object][target] = y + 1 if (y <= x and y <= z) else x + 1 if (
                            x <= y and x <= z) else z + 1
        return distances[len(first)][len(second)]

    def kendallTauDistance(self, object, target):
        """Compute the Kendall tau distance."""
        n = len(object)
        assert len(target) == n, "Both lists have to be of equal length"
        i, j = numpy.meshgrid(numpy.arange(n), numpy.arange(n))
        a = numpy.argsort(object)
        b = numpy.argsort(target)

        ndisordered = numpy.logical_or(numpy.logical_and(a[i] < a[j], b[i] > b[j]),
                                       numpy.logical_and(a[i] > a[j], b[i] < b[j])).sum()
        return ndisordered

    def kendallTau(self, x, y):
        length = min(len(x), len(y))
        v = 0
        for i in range(length):
            for j in range(i, length):
                a = x[i] < x[j] and y[i] > y[j]
                b = x[i] > x[j] and y[i] < y[j]

                if a or b:
                    v += 1
        return v

    def euclidean_distance(self, object, target, target_size=0):
        # self explanitory
        sum_of_elements = 0
        for i in range(len(object)):
            if type(object[i]) == type(''):
                sum_of_elements += (ord(object[i]) - ord(target[i])) ** 2
            else:
                sum_of_elements += (object[i] - target[i]) ** 2
        return math.sqrt(sum_of_elements)

    def fixed_distance(self, object, target, target_size=0):
        correct = incorrect = 0

        for i in range(len(target)):
            if object[i] == target[i]:
                correct += 1
            elif object[i]!='?':
                incorrect += 1
        return correct, incorrect

    def baldwinss(self, pop_size, tries, num_tries):
        return 1 + ((pop_size - 1) * tries / num_tries)

    def fitness(self, object, target, return_output=True):
        cities, cost_matrix, dimentions, capacity=target[0],target[1],target[2],target[3]
        prints = False
        arr=object.object
        fit = 0
        repo = cities[0]
        prev = arr[0] - 1
        fit += repo.neighb[prev] + repo.neighb[arr[len(arr) - 1] - 1]
        cap_sum = cities[prev].demand
        currPath = [prev]
        allPaths = []
        # print(len(arr))
        for i in range(1, len(arr)):
            # print("Demand of city : ", arr[i], " is ", cities[arr[i] - 1].demand)
            curr = arr[i] - 1
            new_truck_distance = repo.neighb[prev] + repo.neighb[curr]
            straight_distance = cities[prev].neighb[curr]

            # print("New Truck Distance: ", new_truck_distance)
            # print("Straight distance: ", straight_distance)

            cap_sum += cities[curr].demand

            if new_truck_distance < straight_distance or cap_sum >= capacity:
                allPaths.append(currPath)
                currPath = [curr]
                fit += new_truck_distance
                cap_sum = cities[curr].demand
            else:
                currPath.append(curr)
                fit += straight_distance
            # print("Capacity sum is: ", cap_sum)
            prev = curr
        allPaths.append(currPath)

        if prints:
            writ = f"Fitness: {fit}\n"
            counter = 1
            for path in allPaths:
                writ += f"Car {counter}: " + "0 " + "".join(str(x) + " " for x in path) + "0" + "\n"
                counter += 1

            # output_file.write(writ)
        if return_output:
            writ = f"Fitness: {fit}\n"
            counter = 1
            for path in allPaths:
                writ += f"Car {counter}: " + "0 " + "".join(str(x) + " " for x in path) + "0" + "\n"
                counter += 1
        object.solution=writ
        object.fitness=fit
        return fit
