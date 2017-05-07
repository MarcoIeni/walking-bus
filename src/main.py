import json
import os
import sys
import time

import dat_parser
import graph
import output
from timer import MyTimer
import algorithm_thread
from algorithm_thread import AlgorithmThread

CONFIG_FILEPATH= '..' + os.path.sep + 'config.json'

def get_delta(nodes_number):
    """
    Get the delta depending on the number of nodes in the graph.
    The generation of delta has mainly been determined empirically.
    :param nodes_number: number of nodes in the graph
    :return: a list that represents the delta that has been generated
    """
    delta_list = []
    d = 1.05
    if nodes_number > 60:
        while d <= 1.101:
            i_str = "%.2f" % d
            delta_list.append(float(i_str))
            d += 0.01
        while d <= 1.5:
            i_str = "%.2f" % d
            delta_list.append(float(i_str))
            d += 0.02
    else:
        while d <= 2:
            i_str = "%.2f" % d
            delta_list.append(float(i_str))
            d += 0.05
        while d <= 4:
            i_str = "%.2f" % d
            delta_list.append(float(i_str))
            d += 0.2
        while d <= 5.1:
            i_str = "%.2f" % d
            delta_list.append(float(i_str))
            d += 0.5
    return delta_list


with open(CONFIG_FILEPATH) as config_file:
    config_data = json.load(config_file)

N_THREADS = config_data["threads_number"]  # numbers of threads

# The following timeouts and time intervals are in seconds

# After this interval the program stops and the solution file is produced
ABSOLUTE_TIMEOUT = config_data["absolute_timeout"]

# After this interval of time since the start of the program, the threads keep only their best delta
TUNING_TIMEOUT = config_data["tuning_timeout"]

# Time in which if you don't have any improvement you stop the algorithm
IMPROVEMENT_TIMEOUT = config_data["improvement_timeout"]

# How much seconds do you wait every time to update the best solution among all the threads
CHECKING_INTERVAL = config_data["checking_interval"]

absolute_timer = MyTimer(ABSOLUTE_TIMEOUT, "absolute_timer")
absolute_timer.start()

test_file = "pedibus_10"  # edit this if you do not want to pass a command line arg.

file_path = ".." + os.path.sep + "test_instances" + os.path.sep + test_file + ".dat"

if len(sys.argv) > 1:
    file_path = sys.argv[1]

test_file = file_path[:-4]
for i in range(1, len(file_path)):
    if file_path[-i] == os.path.sep:
        path_present = True
        test_file = file_path[-i + 1:-4]
        break


data = dat_parser.get_data(file_path)

gr = graph.Graph(data)  # this object contains the information about the graph and the problem itself

delta = get_delta(gr.n)  # these are the delta to be used at the beginning

print("test_file: " + test_file)
print("delta: " + str(delta))

threads = []
for i in range(0, N_THREADS):
    threads.append(AlgorithmThread(delta, gr))

for t in threads:
    t.start()

tuning_timer = MyTimer(TUNING_TIMEOUT, "tuning_timer")
tuning_timer.start()

improvement_timer = MyTimer(IMPROVEMENT_TIMEOUT, "improvement_timer")
improvement_timer.start()

best_edges = []
min_score = float("inf")
best_delta = 0  # it is not used in the computation, but only to understand with which delta was obtained the best score
result_changed = False

while not improvement_timer.is_expired() and not absolute_timer.is_expired():
    time.sleep(CHECKING_INTERVAL)  # during this interval the thread compute their local best result
    # now I take the best result among the local ones
    for t in threads:
        local_score, local_best_edges, local_best_delta = t.get_best_result()
        if local_score < min_score:
            # the local result is better then the best found since now, so I set the best result to this one
            min_score = local_score
            best_edges = local_best_edges
            best_delta = local_best_delta
            result_changed = True
    if result_changed:
        improvement_timer.reset()
        # I communicate to all the threads which is the best result since now.
        # In this way they will update their local result only if it is better than this one
        for t in threads:
            t.set_best(min_score, best_edges, best_delta)
        result_changed = False
        print("score: " + str(min_score) + "; best delta: " + str(best_delta))
    else:
        print("no improvements found")
    if tuning_timer.is_expired():
        algorithm_thread.store_best = False

for t in threads:
    t.stop_it()

print("best score: " + str(min_score))

# I close all the timers
if not improvement_timer.is_expired():
    improvement_timer.delete()
if not absolute_timer.is_expired():
    absolute_timer.delete()

# I generate the solution file
output.generate_output(best_edges, test_file)
