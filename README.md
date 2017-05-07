# Foundations of Operations Research Challenge: Walking bus

Project repository for a solution of the "Walking Bus Challenge" of the Foundations of Operations Research course of M.Sc. Computer Science and Engineering at Politecnico di Milano.

This challenge consisted in the minimization of the number of chaperons involved in the setup of a walking bus system for an elementary school, respecting some constraints that involved mainly the *distance* between students' houses and school and the *risk* of the roads.

In mathematical terms this problem is translated in a special case of the spanning tree problem, in which you have to **minimize the number of leaves**.

You can see the full assignment material in the `assignment` and `test_instances` directories.

With this solution we arrived fourth out of 36 groups.

## Group members
* Astolfi Pietro;
* Fiorentini Stefano Emanuele;
* Ieni Marco.

## Solver specification
The solver for this Challenge has been made using Python3 programming language.

The solver uses the following additional packages of Python:

* numpy
* Pulp

Once the environment is ready, it is enough to call:

```
python main.py dat_file_path
```

from terminal specifying the file path of the .dat file to use.

## Algorithm Specification
The problem requires to find the *spanning tree* with the minimum number of leaves. This kind of problems are well known and a good and valid approach is to create an algorithm similar to the Depth First Search (for more information, see the work of 2010 and 2014 of Gabor Wiener and Gabor Salamon).

However in our case the graph is *complete*, thus the generation of a new branch occurs only when the constraint on the path length is violated.

So we developed a **randomized-greedy algorithm** that minimizes the number of leaves as much as possible.
It’s based on the known GRASP idea and uses a parameter ‘delta’ that decides the entity of the randomization. The problem with many greedy heuristics is that they always return the same local optimal solution, that may not be the best one. By introducing a delta parameter into the heuristic, a graph algorithm obtain different solutions, and at the end select the best one among them.


In the following lines we state the main steps of the algorithm:

* It starts visiting the graph from the school node (root of the tree) then it has to choose the next node of the current branch among the ones that weren’t visited yet.
* To find the next node to visit at each iteration, our heuristic selects the feasible nodes (the ones that if added to the current path satisfy the path length constraint) and finds the node having minimum distance from the last node visited. Let’s call this distance min_temp_dist.
* It creates a set of candidates nodes among the feasible ones. All candidates must have distance from the last node visited less than the min_temp_dist, multiplied by delta. As we can see, the delta parameter represents the “error” or confidence we use to vary our possible solutions.
* Then, It selects one of the candidate node at random, marks it as visited, adds it to the current path, and it goes to the next iteration.
* If the previously visited node has no feasible nodes (that is, it cannot add a   node to the current path without violating the distance constraint), it means that it is a leaf node: the path is added to the current solution and  the algorithm start again from the root node.
* The algorithm continues to find different trees, changing each time the values of delta provided. If the solution tree is the best one until now, it saves it as the temporary best. When the algorithm stops, it returns the best value found. The stopping condition of the algorithms are the following:
  * An “improvement timer” that expires if no improvements are found after 30 minutes of iterations.
  * An “absolute timer” that expires when the program is executing for more than 59 minutes.

In addition to this, the algorithm has two phases, in which the algorithm uses different values of delta. In the first phase, the algorithm is doing the **tuning** of the delta values, in fact it works with many delta and tries to understand which one give the better result, while in the second phase it uses only the best delta.

Since this process of tuning is purely heuristic, the program uses **threading** in order to work with different sets of "best delta values". In fact each thread will execute independently from each other, periodically sharing his best score, and therefore each thread will end up with its own set of "best delta values". In this way, even if it happens the unlucky case in which in the first phase you find delta values which resulted optimal only for a fortuitous, this will not affect the overall computation, but only the one of the unlucky threads.

## Config file
In the json config file you can find the following parameter:

* threads_number: the number of threads that you want to run;
* absolute_timeout: after this interval the program stops and the solution file is produced;
* tuning_timeout: after this interval of time since the start of the program, the threads keep only their best delta;
* improvement_timeout: time in which if you don't have any improvement you stop the algorithm;
* checking_interval: how much seconds do you wait every time to update the best solution among all the threads.
