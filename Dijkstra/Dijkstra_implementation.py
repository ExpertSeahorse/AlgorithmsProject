from queue import PriorityQueue 
from copy import deepcopy

# constants/globals
state_id = 0
goalKey={
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 5,
    '5': 8,
    '6': 7,
    '7': 6,
    '8': 3,
    '0': 4
}


class Vertex:
    def __init__(self, label, index):
        # index = position in the 3x3 array of the game board
        # label = value of the vertex/tile
        # adjacent = all tiles next to the vertex (populated by the Graph)
        self.index = index
        self.label = int(label)
        self.adjacent = []

    # "overloads" the comparison operators to compare the labels of the Vertices
    def __cmp__(self, other):
        return cmp(self.label, other.label)
    
    # Defines how to print a Vertex
    def __str__(self):
        return f"{self.label}"


class Graph:
    def __init__(self, matrix, prio=0, prev=False, move=False):
        # if type(matrix) = filename: get matrix from file
        self.vertex_arr = []
        if type(matrix) == str:
            self.vertex_arr = self.buildArr(matrix)
        # if type(matrix) = array: just use the given array to populate the new Graph
        # This is kinda like a copy constructor
        else:
            self.vertex_arr = matrix

        self.blanki = [v.label for v in self.vertex_arr].index(0)

        # total manhattan distance of the graph from the goal
        self.val = self.getValue()

        # number of states away from the inital state
        self.prio = prio
        # a link to the previous state
        self.prev = prev
        # str record of the move to reach this state from the prev
        self.prev_move = move

        # assign the state with an id for determining number of states used
        global state_id
        self.id = state_id
        state_id += 1

    def buildArr(self, filename):
        # digest the content of filename into a Graph object
        with open(filename, 'r') as fin:
            arr = fin.read().splitlines()
            li = []
            i=0
            for row in arr:
                for j in row.split('   '):
                    li.append(Vertex(j, i))
                    i += 1
            
        # fill out adjacent vertices
        for i in range(len(li)):
            vtx = li[i]
            # Add moveLeft
            if i not in [0, 3, 6]:
                vtx.adjacent.append(li[i-1])
            # Add moveRight
            if i not in [2, 5, 8]:
                vtx.adjacent.append(li[i+1])
            # Add moveUp
            if i not in [0, 1, 2]:
                vtx.adjacent.append(li[i-3])
            # Add moveDown
            if i not in [6, 7, 8]:
                vtx.adjacent.append(li[i+3])

        return li
    def getValue(self):
        # generate the 'value' of the state using the sum of all the
        # manhattan distances of the tiles from their current location to 
        # thier solution location defined in the goalKey dict
        total = 0
        for v in self.vertex_arr:
            goal = goalKey[str(v.label)]
            i = v.index
            t=0
            while(goal != i):
                # if the tile is in the middle, the manhattan distance is calculated from 2 rather than 3
                m=3
                if i in [1, 4, 7]:
                    m=2
                # if the goal is in a lower row, shift down
                if goal >= i+m:                    
                    i += 3
                # if the goal is in a higher row, shift up
                elif goal <= i-m:
                    i -= 3

                # if the goal is on the same row...

                # if goal is to the right 
                elif goal > i:
                    # and the tile is not already on the right edge, move right
                    if i not in [2, 5, 8]:
                        i += 1
                    # else move up
                    else:
                        i += 3
                
                # if goal is to the left
                elif goal < i:
                    # and the tile is not already on the left edge, move left 
                    if i not in [0, 3, 6]:
                        i -= 1
                    # else move down
                    else:
                        i -= 3
                # add 1 to the tally of the number of missing numbers
                total += 1
        return total
    
    def swap(self, i, j):
        # Return a copy of the array, after swapping the tiles in index i and j
        temp_arr = deepcopy(self.vertex_arr)
        temp_arr[i], temp_arr[j] = temp_arr[j], temp_arr[i]
        temp_arr[i].index = i
        temp_arr[j].index = j

        return temp_arr

    # Overload the == operator (checking for duplicate states)
    def __eq__(self, other):
        return self.vertex_arr == other.vertex_arr
    def __cmp__(self, other):
        return cmp(self.val, other.val)
    def __str__(self):
        if self.prev:
            return (
                f"{'  '.join(str(v) for v in self.vertex_arr[:3])}\n"
                f"{'  '.join(str(v) for v in self.vertex_arr[3:6])}\n"
                f"{'  '.join(str(v) for v in self.vertex_arr[6:])}\n"
                f"prio of graph: {self.prio}\n"
                f"prev graph: {self.prev.id}\n"
                "------------"
            )
        else:
            return (
                f"{'  '.join(str(v) for v in self.vertex_arr[:3])}\n"
                f"{'  '.join(str(v) for v in self.vertex_arr[3:6])}\n"
                f"{'  '.join(str(v) for v in self.vertex_arr[6:])}\n"
                f"prio of graph: {self.prio}\n"
                "------------"
            )


def Dijkstra(init):
    open_states = [init]
    closed_states = []

    while len(open_states):
        s = open_states[0]
        prio = open_states[0].prio
        for state in open_states:
            if state.prio < prio:
                prio = state.prio
                s = state

        # if the state is done, just remove it
        if s in closed_states:
            continue
        # if at the goal state, we have the shortest path
        if s.val == 0:
            break
        
        #else build out child states and append them to open
        closed_states.append(s)
        open_states.remove(s)
        blanki = s.blanki
        states=[]

        # Create a new Graph for every possible move at the open state 
        # new Graph = curr Graph but prio=curr+moved_tile, prev=curr_Graph, array= curr_after_swap
        if blanki not in [0, 1, 2]:
            states.append(Graph(s.swap(blanki, blanki-3), s.prio+s.vertex_arr[blanki-3].label, s, "move blank up"))
        if blanki not in [6, 7, 8]:
            states.append(Graph(s.swap(blanki, blanki+3), s.prio+s.vertex_arr[blanki+3].label, s, "move blank down"))
        if blanki not in [0, 3, 6]:
            states.append(Graph(s.swap(blanki, blanki-1), s.prio+s.vertex_arr[blanki-1].label, s, "move blank left"))
        if blanki not in [2, 5, 8]:
            states.append(Graph(s.swap(blanki, blanki+1), s.prio+s.vertex_arr[blanki+1].label, s, "move blank right"))
        
        # for the 4 new possible states, filter out duplicates
        for state in states:
            exists = False

            # search for duplicate matrix configurations in the closed states
            for c in closed_states:
                diff = False
                for i in range(9):
                    if state.vertex_arr[i].label != c.vertex_arr[i].label:
                        diff = True
                        break
                if not diff:
                    exists = True

            if not exists:
                open_states.append(state)
                continue

            # search for duplicate matrix configurations in the open states
            for o in open_states:
                # if they are the same state and the new graph is closer to the initial state, overwrite the old state
                if state.vertex_arr == o.vertex_arr:
                    exists = True
                    if state.prio > o.prio:
                        o.prio = state.prio
                        o.prev = state.prev
                        o.prev_move = state.prev_move
                    break
            if not exists:
                open_states.append(state)

    # if there are no more possible states, the algorithm failed 
    else:
        return "no path found"

    # get the total number of created states, the priority of the final state (=cost), and the moves needed to reach it
    prev = []
    prev_moves = []
    print("Total states observed:", state_id)
    while s.prev:
        prev_moves.append(s.prev_move)
        s = s.prev
    return s.prio, prev_moves[::-1]

# if running this file directly, run the algorithm on the first graph
if __name__ == "__main__":
    print(Dijkstra(Graph(matrix='graph1')))
