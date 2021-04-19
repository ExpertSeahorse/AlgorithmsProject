import re
import sys
import numpy as np
from time import time

global min_cost 
global min_depth
min_depth = 1000000000
min_cost = 1000000000

class Node: 
    def __init__(self, board):
        self.board = tuple(board)
        self.parent = None
        self.neighbors = []
        self.operation = " "
        self.cost = 0
        self.goal = []
        self.depth = 0
        self.zero = self.getZero()

    def getZero(self):
        curboard =  self.board
        index = curboard.index(0)
        return index

    def goalReached(self):
        return list(self.board) == self.goal

#Move up and create child from new board 
    def left(self):
        blank = self.zero
        if(blank == 3) or (blank == 6) or (blank == 9):
            return None
        else: 
            newBoard = list(self.board)
            cost = newBoard[blank -1]
            newBoard[blank], newBoard[blank-1] = newBoard[blank -1], newBoard[blank]
            newNeighbor = Node(newBoard)
            newNeighbor.goal = self.goal
            self.neighbors.append(newNeighbor)
            newNeighbor.parent = self
            newNeighbor.operation = "left"
            newNeighbor.depth = self.depth + 1
            newNeighbor.cost = self.cost + cost

#Move right and create child from new board 
    def right(self):
        blank = self.zero
        if(blank ==2 or blank ==5 or blank == 8):
            return None
        else: 
            newBoard = list(self.board)
            cost = newBoard[blank +1]
            newBoard[blank], newBoard[blank+1] = newBoard[blank +1], newBoard[blank]
            newNeighbor = Node(newBoard)
            newNeighbor.goal = self.goal
            self.neighbors.append(newNeighbor)
            newNeighbor.parent = self
            newNeighbor.operation = "right"
            newNeighbor.depth = self.depth + 1
            newNeighbor.cost = self.cost + cost

#Move up and create child based on new board configuration            
    def up(self):
        blank = self.zero
        if((blank - 3) <= 0):
            return None
        else :
            newBoard = list(self.board)
            cost = newBoard[blank -3]
            newBoard[blank], newBoard[blank-3] = newBoard[blank -3], newBoard[blank]
            newNeighbor = Node(newBoard)
            newNeighbor.goal = self.goal
            self.neighbors.append(newNeighbor)
            newNeighbor.parent = self
            newNeighbor.operation = "up"
            newNeighbor.depth = self.depth + 1
            newNeighbor.cost = self.cost + cost
            
#Move down and create new child based on board configuration
    def down(self):
        blank = self.zero
        if((blank + 3) >= 9):
            return None
        else:
            newBoard = list(self.board)
            cost = newBoard[blank +3]
            newBoard[blank], newBoard[blank+3] = newBoard[blank +3], newBoard[blank]
            newNeighbor = Node(newBoard)
            newNeighbor.goal = self.goal
            self.neighbors.append(newNeighbor)
            newNeighbor.parent = self
            newNeighbor.operation = "down"
            newNeighbor.depth = self.depth + 1
            newNeighbor.cost = self.cost + cost
#Calls the helper functions to make valid moves 
    def getNeighbors(self):
        self.zero
        self.left()
        self.up()
        self.right()
        self.down()
        chldr = self.neighbors
        return(reversed(chldr)) # have to reverse the order since lists pop from the right 
        
#Performs depth first search, given the starting point and end point 
def dfs(initial_state, goal_state, l):
    global min_cost
    global min_depth
    startNode = Node(initial_state)
    startNode.goal = goal_state
    stack = []
    stack.append(startNode)
    explored = set()
    limit = l
    while(stack):
        
        cur_node = stack.pop()
        explored.add(cur_node.board)
        
        if(cur_node.goalReached()):
            if cur_node.cost < min_cost:
                min_cost = cur_node.cost
            return (cur_node)
    
        for N in cur_node.getNeighbors():
            if (N.board not in explored and N not in stack and N.depth < limit):
                stack.append(N)

def main():
    #load the initial state into a list
    print("Which board would you like to find the lowest cost to? Enter an number based on the options below")
    print("1.Board 1 \n 2.Board 2")

    c = int(input())
    if (c == 1):
        filename = 'board1.txt'
    if (c == 2):
        filename = 'board2.txt'
    else:
        print("Please select a number from the menu options")

    file = open(filename, 'r')
    istate = str(file.readlines()[0:3])
    Istate = re.findall(r"[-+]?\d*\.\d+|\d+", istate)
    Istate = list([ int(x) for x in Istate ])

    #load the goal state into a list
    file.close()
    file = open(filename, 'r')
    gstate = str(file.readlines()[4:7])
    Gstate = re.findall(r"[-+]?\d*\.\d+|\d+", gstate)
    Gstate = list([ int(x) for x in Gstate ])
    
    #Prints the goal and Initial States 
    Gs = np.array(Gstate)
    Is = np.array(Istate)
    print("Initial State: \n",Is.reshape(3,3))
    print("Goal State: \n",Gs.reshape(3,3))
    print("Performing DFS...")        
    
    t = 0
    ##t0 = time()
    while(t < 16):
        dfs(Istate,Gstate,t)
        t = t+1
    ##t1 = time()


    print("Solution: The shortest path cost = ", min_cost) 
    #print("Time:", t1-t0)
    

if __name__ == '__main__':
    main()