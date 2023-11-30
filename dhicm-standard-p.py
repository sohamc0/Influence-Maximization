import networkx as nx
import numpy as np
import time
import sys

def select_seed_nodes(G, k, p):
    S = set()
    V = set(G.nodes())  # Assuming G is a NetworkX graph or a similar graph representation
    ddv = {v: G.in_degree(v) for v in V}

    for i in range(k):
        u = max((v for v in V - S), key=lambda v: ddv[v])
        S.add(u)

        for v in G.predecessors(u):
            if v not in S:
              if u in G.predecessors(v):
                ddv[v] = G.in_degree(v) - 1 - ((G.in_degree(u) - 1) * p)
    return S

def ICM(graph_object,S,mc,p):
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
            success = np.random.uniform(0,1,len(targets)) < p
            new_ones = list(np.extract(success, sorted(targets)))

            # 3. Find newly activated nodes and add to the set of activated nodes
            new_active = list(set(new_ones) - set(A))
            A += new_active

        spread.append(len(A))

    return(np.mean(spread),A)

def propagate(g, new_active):
    targets = []
    for node in new_active:
      targets += g.predecessors(node)

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
s = select_seed_nodes(G, int(sys.argv[2]), 0.1)
print("Time getting seed set: ", time.time() - start_time)





start_time = time.time()
#getting mean spread
(mean_spread, A) = ICM(G, list(s), int(sys.argv[3]), 0.1)
print("Mean spread: ", mean_spread)
print("Duration: ", time.time() - start_time)