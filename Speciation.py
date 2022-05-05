# given a hash table that has all distances between 2 genes find the spiecies
# given a threshhold
# given a population
import random

import numpy

from Genetic import genetic_algorithem


# todo: figure out the threshold
def spicieation_threshold(most_recent_thresh, minimal_distance, numOfspiecies, spiecies_count):
    Multiplier = 1
    up_down = True if numOfspiecies > spiecies_count else False if numOfspiecies < spiecies_count else -1
    k = Multiplier * (
        most_recent_thresh + minimal_distance if up_down else most_recent_thresh - minimal_distance) if up_down != -1 else most_recent_thresh
    print(k)
    return k


def Minimal_distance(gene, distance_function, prob_spec):
    Gene2 = prob_spec()
    Gene2.object = gene.object
    Gene2.mutate(len(gene.object), Gene2, 1) if type(Gene2.object) == str else Gene2.mutate(len(gene.object), Gene2, 2)
    return distance_function(gene.object, Gene2.object)


class SpeciationType:
    def __init__(self):
        self.type = {1: self.threshhold_speciation, 2: self.optimal_k_clustering}

    # threshold functions:

    def threshhold_speciation(self, hash, thresh, pop):
        # the genes that are put in a group are signified by  a true value in the used array
        used = numpy.array([False for i in range(len(pop))])
        bins = []
        counter = 0
        for gene in pop:
            spiecies = []
            # go over the spiecies and arrange them according to the similarities
            for index, gene2 in enumerate(pop):

                strings = gene.hash(gene2)
                strings2 = gene2.hash(gene)
                dist = hash[strings] if strings in hash.keys() else hash[strings2]
                if dist <= thresh and not used[index]:
                    spiecies.append(gene2)
                    gene2.spiecy = counter
                    used[index] = True
            if spiecies != []:
                bins.append(spiecies)
                counter += 1
        return bins

    # k means functions
    # given centroids and population, hash of distances create the clusters
    def k_means_clustering(self, hash, k, pop):

        # select k centroids by random
        k1 = k
        centroids = random.sample(pop, k1)
        centroids2 = []
        while (True):
            # appoint clusters
            clusters = [[] for i in range(k1)]
            # appoint cluster means
            clusters_means = [[] for i in range(k1)]
            distances = numpy.array([None for i in range(k1)])
            clusters, clusters_means = self.sub_k_means(hash, pop, centroids, clusters, clusters_means, distances)
            # find new centroids
            centroids2 = centroids
            for j in range(k1):
                # given clusters and its mean get the new clusters index , i.e cj
                cluster_distances = numpy.asarray(clusters_means[j])
                cj = self.find_closest_val(cluster_distances,
                                           cluster_distances.mean() if cluster_distances.any() else 0)
                # assign the new centroid
                if cj != -1:
                    centroids2[j] = clusters[j][cj]
            if centroids2 == centroids:
                # i.e. if we the centroids are the same then we have reached a conclusion on k
                break
        return clusters, self.silhouette_score(clusters, hash)

    def optimal_k_clustering(self, hash, k, pop):
        for k1 in range(3, len(pop)):
            groups, sillo_score = self.k_means_clustering(hash, k1, pop)
            if sillo_score:
                break
        return groups

    def sub_k_means(self, hash, pop, centroids, clusters, clusters_means, distances):
        for gene in pop:
            # get distances from each cluster
            for index, centroid in enumerate(centroids):
                strings = gene.hash(centroid)
                strings2 = centroid.hash(gene)
                distances[index] = hash[strings] if strings in hash.keys() else hash[strings2]
            # append the gene to the closest cluster
            clusters[distances.argmin()].append(gene)
            # distance from centroid
            clusters_means[distances.argmin()].append(distances[distances.argmin()])
            # print(clusters, cluster_means)
        return clusters, clusters_means

    # finds the closest distance from the centroid
    def find_closest_val(self, array, value):
        return (numpy.abs(array - value)).argmin() if array.any() else -1

    def silhouette_score(self, clusters, hash):
        a = numpy.array([None for i in range(len(clusters))])
        for index, cluster in enumerate(clusters):
            diversity = []
            if cluster != []:
                for gene in cluster:
                    distance = 0
                    for gene2 in cluster:
                        # strings = ''.join(gene.object + gene2.object)
                        # strings2 = ''.join(gene2.object + gene.object)
                        strings = gene.hash(gene2)
                        strings2 = gene2.hash(gene)
                        distance += hash[strings] if strings in hash.keys() else hash[strings2]
                    diversity.append(distance / len(cluster))
            # distance between each point within a cluster
            diversity = numpy.array(diversity)
            # average intra cluster distance
            a[index] = diversity.mean() if diversity.any() else 0
            # average inter-cluster distance
        a2 = numpy.array([i for i in a if i])
        b = a2.mean()
        # for each cluster silhouette score is
        sil = numpy.array([(b - a1) / max(a1, b) for a1 in a2])
        # array with high values as True and low values as false
        values = sil > 0
        # if mor than half of the clusters have a high sellohet value return true i.e k is optimal ,else false
        return True if values.sum() > len(a2) // 2 else False

        # mean of each cluster


# the general idea is to create 2 genetic algorithims one that works on a given population and given elite members
# the second one uses the first class to work on each spiecy and then adds the solutions together
class mate_for_spiecies(genetic_algorithem):
    def __init__(self, target, tar_size, pop_size, problem_spec, crosstype, fitnesstype, selection,
                 serviving_mechanizem, mutation, gene_dist, mutation_probability=0):
        genetic_algorithem.__init__(self, target, tar_size, pop_size, problem_spec, crosstype, fitnesstype, selection,
                                    serviving_mechanizem, mutation, gene_dist, mutation_probability)

    def mate_pop(self, population, gen, elite_members):
        self.population = population
        self.pop_size = len(self.population)
        self.fitness_array = numpy.zeros((self.pop_size))
        self.buffer = list(range(len(population) - elite_members))  # create buffer with appropriate size
        self.propablities_rank_based()
        self.cross(0, gen, self.population, len(self.buffer))
        return self.buffer


class Genetic_speciation(genetic_algorithem):

    def __init__(self, target, tar_size, pop_size, problem_spec, crosstype, fitnesstype, selection,
                 serviving_mechanizem, mutation, gene_dist, specieation, mutation_probability=0):
        genetic_algorithem.__init__(self, target, tar_size, pop_size, problem_spec, crosstype, fitnesstype, selection,
                                    serviving_mechanizem, mutation, gene_dist, mutation_probability)
        self.mate_for_spiecies = mate_for_spiecies(target, tar_size, pop_size, problem_spec, crosstype, fitnesstype,
                                                   selection,
                                                   serviving_mechanizem, mutation, gene_dist, mutation_probability)
        self.groups = []
        self.speciation = SpeciationType().type[specieation]
        self.speciationType = specieation
        # threshold speciation factor to control threshold
        self.distance_factor = 0
        self.threshold = 0
        self.spiecies_count = 0.15 * pop_size

    # this function returns an array for each spiecy , how many are elite
    # so that we can choose the appropriate ammount of genes from speciy and so that the population size stayes the same
    def how_many_of_each_speicy(self, size):

        sp = [0 for i in range(len(self.groups))]
        for i in range(size):
            sp[self.population[i].spiecy] += 1
        return sp

    # uses a function to devide population into spiecies
    # def threshold_speciation(self, threshold):
    #     return threshhold_speciation(self.Distance_hash, threshold, self.population)

    def mate(self, gen):
        esize = self.serviving_genes(gen)
        # cross function for intial GA algo
        elite_individuals = self.how_many_of_each_speicy(esize)
        for index, group in enumerate(self.groups):
            temp_buffer = self.mate_for_spiecies.mate_pop(group, gen, elite_individuals[index])
            self.buffer[esize:esize + len(group) - elite_individuals[index]] = temp_buffer[:]
            esize += len(group) - elite_individuals[index]

    def init_population(self):
        super(Genetic_speciation, self).init_population()
        # if threshold speciation
        if self.speciationType == 1:
            self.distance_factor = Minimal_distance(self.population[0], self.gene_dist, self.prob_spec)
        else:
            # used as k
            self.threshold = int(0.05 * self.pop_size)

    def algo(self, i):
        self.calc_diversity()  # calculate fitness
        if i == 0:
            self.threshold = self.pop_diversity if self.speciationType == 1 else int(0.05 * self.pop_size)

        self.sort_by_fitness()
        # self.groups = self.threshold_speciation(self.pop_diversity) #devide genes to spiecies
        self.groups = self.speciation(self.Distance_hash, self.threshold, self.population)
        num_of_clusters = len(self.groups)
        self.threshold = spicieation_threshold(self.threshold, self.distance_factor, num_of_clusters,
                                               self.spiecies_count) if self.speciationType == 1 else self.threshold
        self.propablities_rank_based()
        self.mate(i)  # mate the population together
        self.population, self.buffer = self.buffer, self.population  # // swap buffers
        self.solution = self.population[0]
        self.Distance_hash = {}
        print("\nnumber of groups\n", num_of_clusters)
        print("\nselection pressure:", self.selection_pressure, "  Diversity: ", self.pop_diversity)
