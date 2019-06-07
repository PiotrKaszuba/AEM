from Code.Methods.LocalSearch import LocalSearch
import time
import numpy as np
import copy as cp
from operator import attrgetter
from Code.Methods.Nearest import

class Elite:
    def __init__(self,start_population,population_size):
        self.population_size = population_size
        self.population = self.get_pure_population(start_population)


    def get_pure_population(self,population):
        elite_pop = sorted(population, key=attrgetter('metric'))[:self.population_size]
        return


    def recombination_local_search(self, max_iters=100, ttg=None):
        currentTime = 0
        iters = 0
        while (True):
            start = time.time()

            iters += 1
            print(str(iters) + ": Time: " + str(time.time() - start))

            candidat = np.random.choice(self.population,2)
            newItem = None  #Tu funkcja Piotra
            newItem.metric = round(newItem.metric,7)
            if not (any(x.metric == newItem.metric for x in self.population)):
                self.population.append(newItem)
                self.get_pure_population(self.population)

            end = time.time()
            currentTime += end - start
            print(currentTime)
            if (ttg is not None and currentTime > ttg) or (ttg is None and iters == max_iters):
                breakadd
        return max(self.population, key=attrgetter('metric')).countMetric(True)
