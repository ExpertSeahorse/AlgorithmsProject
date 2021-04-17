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
        self.index = index
        self.label = int(label)
        self.adjacent = []

    def __cmp__(self, other):
        return cmp(self.label, other.label)
    def __str__(self):
        return f"{self.label}"


class Graph:
    def __init__(self, matrix, prio=0, prev=False, move=False):
        self.vertex_arr = []
        if type(matrix) == str:
            self.vertex_arr = self.buildArr(matrix)
        else:
            self.vertex_arr = matrix

        self.blanki = [v.label for v in self.vertex_arr].index(0)
        self.val = self.getValue()
        self.prio = prio
        self.prev = prev
        self.prev_move = move
        global state_id
        self.id = state_id
        state_id += 1

    def buildArr(self, filename):
        with open(filename, 'r') as fin:
            # Get graph from the file + add each number to list as Vertex object
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
            #print("vtx:", vtx, "list:", [str(v) for v in vtx.adjacent])

        return li
    def getValue(self):
        total = 0
        for v in self.vertex_arr:
            goal = goalKey[str(v.label)]
            i = v.index
            t=0
            while(goal != i):
                m=3
                if i in [1, 4, 7]:
                    m=2
                if goal >= i+m:                    
                    i += 3
                elif goal <= i-m:
                    i -= 3
                elif goal > i:
                    if i not in [2, 5, 8]:
                        i += 1
                    else:
                        i += 3
                elif goal < i:
                    if i not in [0, 3, 6]:
                        i -= 1
                    else:
                        i -= 3
                total += 1
        return total
    def swap(self, i, j):
        temp_arr = deepcopy(self.vertex_arr)
        temp_arr[i], temp_arr[j] = temp_arr[j], temp_arr[i]
        temp_arr[i].index = i
        temp_arr[j].index = j

        return temp_arr

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
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
    #print(init)
    open_states = [init]
    closed_states = []

    while len(open_states):
        s = open_states[0]
        prio = open_states[0].prio
        for state in open_states:
            if state.prio < prio:
                prio = state.prio
                s = state
        #print(s.id)
        if s in closed_states:
            continue
        # if at the goal state, we have the shortest path
        if s.val == 0:
            break
        
        #print(s)
        #else build out child states and append them to open
        closed_states.append(s)
        open_states.remove(s)
        blanki = s.blanki
        states=[]
        if blanki not in [0, 1, 2]:
            states.append(Graph(s.swap(blanki, blanki-3), s.prio+s.vertex_arr[blanki-3].label, s, "move blank up"))
        if blanki not in [6, 7, 8]:
            states.append(Graph(s.swap(blanki, blanki+3), s.prio+s.vertex_arr[blanki+3].label, s, "move blank down"))
        if blanki not in [0, 3, 6]:
            states.append(Graph(s.swap(blanki, blanki-1), s.prio+s.vertex_arr[blanki-1].label, s, "move blank left"))
        if blanki not in [2, 5, 8]:
            states.append(Graph(s.swap(blanki, blanki+1), s.prio+s.vertex_arr[blanki+1].label, s, "move blank right"))
        
        for state in states:
            exists = False
            for c in closed_states:
                #print("s:", [str(v) for v in state.vertex_arr], "c:", [str(v) for v in c.vertex_arr])
                diff = False
                for i in range(9):
                    if state.vertex_arr[i].label != c.vertex_arr[i].label:
                        diff = True
                        break
                if not diff:
                    exists = True
                    #print("AHHH", '\n', state )
                        
            for o in open_states:
                if state.vertex_arr == c.vertex_arr:
                    exists = True
                    if state.prio > c.prio:
                        c.prio = state.prio
                        c.prev = state.prev
                        c.prev_move = state.prev_move
                    break
            if not exists:
                open_states.append(state)
    else:
        return "no path found"
    
    #print(s)

    cost = s.prio
    prev = []
    prev_moves = []
    while s.prev:
        prev_moves.append(s.prev_move)
        s = s.prev
    return cost, prev_moves[::-1]


if __name__ == "__main__":
    print(Dijkstra(Graph(matrix='graph1')))
