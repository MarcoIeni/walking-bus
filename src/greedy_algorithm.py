import random

ROOT = 0


def find_next(delta, graph, previous_node, not_visited, path_length):
    """
    this function finds the next node to add to the path.
    :param delta: the delta that you want to use to perform this iteration. It decides the entity of the randomization.
    :param graph: the object that contains the information about the graph
    :param previous_node: the previous node in the path
    :param not_visited: nodes that have not been visited yet
    :param path_length: the current path length
    :return: the next node to add to the path
    """

    curr_min_path_length =  float("inf")

    # distance between the previous_node and the node that is closer to it among the not visited ones
    curr_prev_node_min_distance = float("inf")

    acceptable_nodes = []  # nodes that you can add to the current path
    for node_x in not_visited:
        new_path_length = path_length + graph.get_distance(previous_node, node_x)
        node_x_min_distance = graph.get_root_distance(node_x)

        if new_path_length < node_x_min_distance * graph.alpha:  # the node if feasible
            acceptable_nodes.append(node_x)
            if new_path_length < curr_min_path_length:
                curr_min_path_length = new_path_length
                curr_prev_node_min_distance = graph.get_distance(previous_node, node_x)

    if acceptable_nodes:  # if there are nodes that you can add to the current path
        best_nodes = []
        # I select only the nodes that has a distance from the previous node which
        # is <= than curr_prev_node_min_distance * delta
        for node_x in acceptable_nodes:
            new_node_distance = graph.get_distance(previous_node, node_x)
            if new_node_distance <= curr_prev_node_min_distance * delta:
                best_nodes.append(node_x)

        # I select one node randomly among the best ones
        rand = random.randint(0, len(best_nodes) - 1)
        return best_nodes[rand]
    else:
        return -1


def min_distance_delta(graph, delta):
    """
    It executes an iteration of the algorithm and returns the score and the edges associated to it.
    :param graph: the graph on which you want to apply the algorithm
    :param delta: the delta that you want to use
    :return: the score and the edges of this solution
    """
    previous = ROOT
    curr_path_length = 0
    nodes_not_visited = set(range(1, graph.n + 1))
    edges = []
    leaves_counter = 1  # I initialize this to one to add the last one

    while nodes_not_visited:  # while nodes_not_visited is not empty
        next_node = find_next(delta, graph, previous, nodes_not_visited, curr_path_length)
        if next_node != -1:  # I found a feasible node that can be added to the current path
            nodes_not_visited.remove(next_node)
            new_edge = [previous, next_node]
            edges.append(new_edge)
            previous = next_node
            curr_path_length += graph.get_edge_distance(new_edge)
        else:  # you cannot add other nodes to the current path, so I create a new path starting from the root
            curr_path_length = 0
            previous = ROOT
            leaves_counter += 1

    # I compute the score
    risk = graph.get_risk(edges)
    score = str(leaves_counter) + "." + str(risk).replace(".", "")
    return float(score), edges
