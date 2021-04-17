from Dijkstra_implementation import *
import time

# sample graph 1:
start = time.time()
print("Graph 1:")
print(Dijkstra( Graph('graph1') ))
print("exec time:", time.time()-start)

# sample graph 2:
start = time.time()
print("\nGraph 2:")
print(Dijkstra( Graph('graph2') ))
print("exec time:", time.time()-start)
