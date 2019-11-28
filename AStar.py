import numpy as np
import heapq

EMPTY = 0
START = np.array([
    [2, 8, 3],
    [1, 6, 4],
    [7, 0, 5],
])
GOAL = np.array([
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5],
])

openList = []
closedList = []
operator = ["Up","Down", "Left", "Right"]


def distance(current):
    cost = 0
    for i in range(1,9):
        index = np.where(GOAL == i)
        index_current = np.where(current == i)
        cost += abs(index_current[0]-index[0]) + abs(index_current[1]-index[1])
    return cost[0]


class Node:

    def __init__(self, state, parent, move, depth, previousCosts):
        self.expectedCosts = distance(state)
        self.previousCosts = previousCosts
        self.costs = self.expectedCosts + self.previousCosts
        self.parent = parent
        # Welches Kommando wird ausgeführt
        self.move = move
        self.state = state
        self.depth = depth

    def __str__(self):
        return "state:\n %s,\n costs: %i" % (self.state,self.costs)

    def __lt__(self, other):
        return self.costs, other.costs

    def __eq__(self, other):
        return self.state == other.state

def aStart():
    global openList
    global closedList

    root = Node(START, None, None, 0, 0)
    goal = Node(GOAL, None,None,None,None)
    heapq.heappush(openList,root)
    while True:
        currentNode = heapq.heappop()
        if currentNode == goal:
            return get_path_fom_node(currentNode)

        closedList.append(currentNode)
        expandNode(currentNode)


def expandNode(node):
    global openList
    global closedList

    while node.parent is not None:
        parent = node.parent
        if parent in closedList:
            continue


def findNeighbors(node):
    global operator

    neighbors = list()
    neighbors.append(Node(move(node.state, operator[0]), node, 1, node.depth + 1))  # Up
    neighbors.append(Node(move(node.state, operator[1]), node, 2, node.depth + 1))  # Down
    neighbors.append(Node(move(node.state, operator[2]), node, 3, node.depth + 1))  # Left
    neighbors.append(Node(move(node.state, operator[3]), node, 4, node.depth + 1))  # Right
    nodes = [neighbor for neighbor in neighbors if neighbor.state]

    return nodes


def puzzleSize():
    global puzzleLen, boardSide, start_state
    puzzleLen = len(start_state)
    boardSide = int(puzzleLen ** 0.5)


def move(state, operator):
    newState = np.copy(state)

    # Where findet index und gibt zurück (array([pos X]), array([pos Y])
    i = np.where(newState == 0)
    xPos = i[0][0]
    yPos = i[1][0]

    if operator == "Up":

        if yPos != 0:
        # Wenn ganz oben also X = 0 dann geht move nach oben nicht
            temp = newState[xPos][yPos-1]
            newState[xPos][yPos-1] = newState[xPos][yPos]
            newState[xPos][yPos] = temp

            return newState
        else:
            return None

    if operator == "Down":

        if i not in range(puzzleLen - boardSide, puzzleLen):

            temp = newState[i + boardSide]
            newState[i + boardSide] = newState[i]
            newState[i] = temp

            return newState
        else:
            return None

    if operator == "Left":
        if xPos != 0:

            temp = newState[xPos- 1][yPos]
            newState[xPos- 1][yPos] = newState[xPos][yPos]
            newState[xPos][yPos] = temp

            return newState
        else:
            return None

    if operator == "Right":
        if xPos != boardSide:

            temp = newState[xPos + 1][yPos]
            newState[xPos + 1][yPos] = newState[xPos][yPos]
            newState[xPos][yPos] = temp
            
            return newState
        else:
            return None



def f(node):
    # h(f) + c(parent,node) + g(node)
    distance(node) + 1 + node.depth


def get_path_fom_node(node):
    pass

if __name__ == "__main__":
    puzzleSize()
    aStart()