import numpy as np
import heapq

EMPTY = 0
START = None
root = None
openList = []
closedList = []
boardSide = 3


class Stadt:

    def __init__(self, name, entfernung):
        self.name = name
        self.angrenzend = []
        self.entfernung = entfernung
        self.fWert = 0
        self.vorgaenger = None

    def set_angrenzend(self, staedte):
        self.angrenzend = staedte

    def set_vorgaenger(self, vg):
        self.vorgaenger = vg

    def __str__(self):
        return "%s, Entfernunung nach Würzburg %i" % (self.name, self.entfernung)

    def __lt__(self, other):
        return self.costs, other.costs

    def __eq__(self, other):
        return str(self.state) == str(other.state)


SB = Stadt("Saarbrücken", 222)
KL = Stadt("Karlsruhe", 140)
HB = Stadt("Heilbronn", 87)
KA = Stadt("Kaiserslautern", 158)
FRA = Stadt("Frankfurt", 96)
LH = Stadt("Ludwigshafen", 108)
WB = Stadt("Würzburg", 0)

KL.set_angrenzend([{
    "next": HB,
    "kosten": 84,
}, ])


def aStar():
    global openList
    global closedList
    global root

    root = Node(START, None, None, 0, 0)
    goal = Node(GOAL, None, None, None, 0)
    heapq.heappush(openList, root)
    while openList:

        if currentNode == goal:
            return currentNode

        closedList.append(currentNode)
        expandNode(currentNode)
    raise Exception("No solution found")


def expandNode(node):
    global openList
    global closedList

    neighbors = findNeighbors(node)
    for neighbor in neighbors:

        tentative_g = node.depth + 1
        indexNeighbour = -1
        if neighbor in openList:
            indexNeighbour = openList.index(neighbor)
            if openList[indexNeighbour].depth <= tentative_g:
                continue
        neighbor.parent = node
        if indexNeighbour != -1:
            openList[indexNeighbour].costs = f(neighbor)
        else:
            openList.append(neighbor)


def findNeighbors(node):
    global operator

    neighbors = list()
    neighbors.append(Node(move(node.state, operator[0]), node, 1, node.depth + 1, node.costs))  # Up
    neighbors.append(Node(move(node.state, operator[1]), node, 2, node.depth + 1, node.costs))  # Down
    neighbors.append(Node(move(node.state, operator[2]), node, 3, node.depth + 1, node.costs))  # Left
    neighbors.append(Node(move(node.state, operator[3]), node, 4, node.depth + 1, node.costs))  # Right
    nodes = [neighbor for neighbor in neighbors if neighbor.state is not None]

    return nodes


def move(state, operator):
    newState = np.copy(state)

    # Where findet index und gibt zurück (array([pos X]), array([pos Y])
    i = np.where(newState == 0)
    xPos = i[0][0]
    yPos = i[1][0]

    if operator == "Up":

        if yPos != 0:
            # Wenn ganz oben also X = 0 dann geht move nach oben nicht
            temp = newState[xPos][yPos - 1]
            newState[xPos][yPos - 1] = newState[xPos][yPos]
            newState[xPos][yPos] = temp

            return newState
        else:
            return None

    if operator == "Down":

        if yPos + 1 != boardSide:

            temp = newState[xPos][yPos + 1]
            newState[xPos][yPos + 1] = newState[xPos][yPos]
            newState[xPos][yPos] = temp

            return newState
        else:
            return None

    if operator == "Left":
        if xPos != 0:

            temp = newState[xPos - 1][yPos]
            newState[xPos - 1][yPos] = newState[xPos][yPos]
            newState[xPos][yPos] = temp

            return newState
        else:
            return None

    if operator == "Right":
        if xPos + 1 != boardSide:

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
    currentNode = node
    moves = list()
    while root != currentNode:

        if currentNode.move == 1:
            movement = 'Up'
        elif currentNode.move == 2:
            movement = 'Down'
        elif currentNode.move == 3:
            movement = 'Left'
        else:
            movement = 'Right'

        moves.insert(0, movement)
        currentNode = currentNode.parent

    return moves


if __name__ == "__main__":
    print("Starting")
    endNode = aStar()
    print("Found node")
    path = get_path_fom_node(endNode)
    print(path)
