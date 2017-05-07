import threading
from operator import itemgetter

import greedy_algorithm

BEST_DELTA_PERCENTAGE = 30

store_best = True  # if it is true we are still in the tuning phase


class DeltaManager:
    """
    It keeps track of the best score found with a certain delta, in order to understand which are the local best deltas.
    """

    def __init__(self, deltas):
        self.deltas_score = {}
        self.__init_deltas_score(deltas)

    def __init_deltas_score(self, deltas):
        for d in deltas:
            self.deltas_score[d] = float("inf")

    def update_best(self, delta, score):
        if score < self.deltas_score[delta]:
            self.deltas_score[delta] = score

    def get_best_deltas(self, percentage):
        """
        Returns the deltas that have found the best score.
        Number of deltas returned = total number of deltas * percentage / 100
        :param percentage: determines how many deltas you want to get
        :return: a list that contains the best delta
        """
        num_result = int(len(self.deltas_score) * percentage / 100)
        list_delta = []
        for key, value in self.deltas_score.items():
            list_delta.append([key, value])
        list_delta.sort(key=itemgetter(1))
        best_delta = list_delta[:num_result]
        return [item[0] for item in best_delta]


class AlgorithmThread(threading.Thread):
    """
    It manages the execution of the main algorithm
    """
    def get_best_result(self):
        self.threadLock.acquire()
        result = self.best_score, self.best_edges, self.best_delta
        self.threadLock.release()
        return result

    def set_best(self, score, edges, delta):  # best result among all delta
        self.threadLock.acquire()
        if score < self.best_score:
            self.best_score = score
            self.best_edges = edges
            self.best_delta = delta
        self.threadLock.release()

    def __init__(self, delta, gr):
        threading.Thread.__init__(self)
        self._stopper = threading.Event()
        self.delta = delta  # list of delta used
        self.delta_manager = DeltaManager(self.delta)
        self.gr = gr
        self.best_score = float("inf")
        self.best_edges = []
        self.best_delta = 0  # used only for tuning
        self.threadLock = threading.Lock()
        # Every thread has its own lock, that is needed to synchronize with the main and with itself.
        # Threads works independently with each other

    def stop_it(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.isSet()

    def compute_iteration(self, d):
        score, edges = greedy_algorithm.min_distance_delta(self.gr, d)
        self.threadLock.acquire()
        if score < self.best_score:
            self.best_edges = edges
            self.best_score = score
            self.best_delta = d
        self.threadLock.release()
        return score

    def second_run(self):
        """
        same as run(self) but I don't check the store_best value because I am not in the training phase anymore
        """
        while not self.stopped():
            for d in self.delta:
                self.compute_iteration(d)

    def run(self):
        while not self.stopped():
            for d in self.delta:
                score = self.compute_iteration(d)
                if store_best:
                    self.delta_manager.update_best(d, score)
                else:
                    """
                    I am not in the training phase anymore, so I get only the best delta found since now and I continue
                    the computation with only these deltas.
                    """
                    self.delta = self.delta_manager.get_best_deltas(BEST_DELTA_PERCENTAGE)
                    self.second_run()
