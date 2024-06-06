import networkx as nx
import numpy as np
import time
import sys

def select_seed_nodes(G, k):
    S = set()
    V = set(G.nodes())  # Assuming G is a NetworkX graph or a similar graph representation
    ddv = {v: G.in_degree(v) for v in V}

    for i in range(k):
        u = max((v for v in V - S), key=lambda v: ddv[v])
        S.add(u)

        for v in G.predecessors(u):
            if v not in S:
              if u in G.predecessors(v):
                common_neighbors = set(G.predecessors(v)).intersection(set(G.predecessors(u)))
                p = 0.01 + ((G.in_degree(u) + G.in_degree(v))/G.number_of_nodes()) + (len(common_neighbors)/G.number_of_nodes())
                ddv[v] = G.in_degree(v) - 1 - ((G.in_degree(u) - 1) * p)
    return S

def ICM(graph_object,S,mc):
    """
    Inputs: graph_object: must be networkx directed graph
            S:  List of seed nodes
            p:  Disease propagation probability
            mc: Number of Monte-Carlo simulations,
    Output: Average number of nodes influenced by seed nodes in S
    """

    # Loop over the Monte-Carlo Simulations
    spread = []
    for i in range(mc):

        # Simulate propagation process
        new_active, A = S[:], S[:]
        while new_active:
            # 1. Find out-neighbors(i.e. successor nodes) for each newly active node
            targets = propagate(graph_object, new_active)

            # 2. Determine newly activated neighbors (set seed and sort for consistency)
            np.random.seed(i)
            new_ones = []
            for (curr_target, p) in targets:
              if np.random.uniform(0,1) < p:
                new_ones.append(curr_target)

            # 3. Find newly activated nodes and add to the set of activated nodes
            new_active = list(set(new_ones) - set(A))
            A += new_active

        spread.append(len(A))
        print("mc #", i+1, " done!")

    return(np.mean(spread),A)

def propagate(g, new_active):
    targets = []
    for node in new_active:
      for neighbor in g.predecessors(node):
        common_neighbors = set(G.predecessors(node)).intersection(set(G.predecessors(neighbor)))
        p = 0.01 + ((G.in_degree(node) + G.in_degree(neighbor))/G.number_of_nodes()) + (len(common_neighbors)/G.number_of_nodes())
        targets.append((neighbor, p))

    return targets

# creating graph
file1 = open(str(sys.argv[1]), 'r')
Lines = file1.readlines()
edge_list = []
for line in Lines:
  u_v = line.strip().split()
  edge_list.append((int(u_v[0]), int(u_v[1])))

G = nx.DiGraph()
G.add_edges_from(edge_list)  # using a list of edge tuples




#getting seed nodes using dhicm
start_time = time.time()
s = select_seed_nodes(G, int(sys.argv[2]))
print("Time getting seed set: ", time.time() - start_time)





start_time = time.time()
#getting mean spread
(mean_spread, A) = ICM(G, list(s), int(sys.argv[3]))
print("Mean spread: ", mean_spread)
print("Duration: ", time.time() - start_time)