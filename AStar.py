import numpy as np
import heapq
import time



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
manHeuristic = 'MANHATTAN'
eucHeuristic = 'EUCLID'
root = None
openList = []
closedList = []
operator = ["Up","Down", "Left", "Right"]
boardSide = 3
inverses = 0

heuristic = ''
path = []


def clear():
    global root, openList, closedList, heuristic, path

    root = None
    openList = []
    closedList = []
    heuristic = ''
    path = []

def distance(current):
    global heuristic,eucHeuristic,manHeuristic

    if heuristic == manHeuristic:
        return manhattan(current)
    else:
        return euclidean(current)



def euclidean(current):
    # Berechnet Euklidischen Abstand zum Ziel
    cost = 0
    for i in range(1,9):
        index = np.where(GOAL == i)
        index_current = np.where(current.state == i)
        cost += np.sqrt(np.power(index_current[0][0]-index[0][0],2) + np.power(index_current[1][0]-index[1][0],2))
    return cost


def manhattan(current):
    # Berechnet Manhattandistanz zum Ziel
    cost = 0
    for i in range(1, 9):
        index = np.where(GOAL == i)
        index_current = np.where(current.state == i)
        cost += abs(index_current[0][0] - index[0][0]) + abs(index_current[1][0] - index[1][0])
    return cost


class Node:

    def __init__(self, state, parent, move,  previousCosts):
        self.state = state

        if state is not None:
            self.expectedCosts = distance(self)
            self.previousCosts = previousCosts
            self.costs = distance(self) + previousCosts +1
            self.parent = parent
            # Welches Kommando wird ausgeführt
            self.move = move

    def __str__(self):
        return "state:\n %s,\n costs: %i" % (self.state,self.costs)

    def __lt__(self, other):
        return self.costs < other.costs

    def __gt__(self, other):
        return self.costs > other.costs

    def __le__(self,other):
        return self.costs <= other.costs

    def __ge__(self,other):
        return self.costs >= other.costs

    def __eq__(self, other):
        return str(self.state) == str(other.state)

    def __repr__(self):
        return str(self.state)


def aStar():

    global openList
    global closedList
    global root

    root = Node(START, None, None, 0)
    print("Expected cost:",root.expectedCosts)
    goal = Node(GOAL, None,None,0)

    heapq.heappush(openList,root)
    while openList:

        # Magical Methods der Nodes verweisen beim Vergleich auf die costs Variabel.
        # Nach diesen wird dann sortiert
        openList = sorted(openList, reverse=True)

        currentNode = openList.pop()


        if currentNode == goal:

            return currentNode

        # was in der closedList ist, wurde bereits besucht. Wird im expand geprüft
        closedList.append(currentNode)
        expandNode(currentNode)
    raise Exception("No solution found")


def expandNode(node):
    global openList
    global closedList

    neighbors = find_neighbors(node)

    for neighbor in neighbors:

        # wenn neighbor bereits besucht, beachte ihn nicht
        if neighbor in closedList:
            continue


        indexNeighbour = -1
        if neighbor in openList:
            indexNeighbour = openList.index(neighbor)


        neighbor.parent = node

        if indexNeighbour != -1:
            #Sollte der Pfad zum momentanen State beim betrachteten Neighbor günstiger sein,
            # als der State, der bereits mit einer Koste in der openList vertreten ist,
            # dann wird die Node in der openList ersetzt. Das spielt nur für den späteren Pfad eine Rolle.
            # Sollte eigentlich nur in Grenzfällen vorkommen, die mir gerade nicht einfallen.
            openList[indexNeighbour] = neighbor if neighbor.costs <= openList[indexNeighbour].costs else openList[indexNeighbour]
        else:
            openList.append(neighbor)


def find_neighbors(node):
    #findet Nachbarn
    global operator
    global closedList

    neighbors = list()

    #Nachbar wird aus bestehender Node erstellt und dann noch verschoben
    neighbors.append(Node(move(node.state, operator[0]), node, 1,  node.costs))  # Up
    neighbors.append(Node(move(node.state, operator[1]), node, 2,  node.costs))  # Down
    neighbors.append(Node(move(node.state, operator[2]), node, 3,  node.costs))  # Left
    neighbors.append(Node(move(node.state, operator[3]), node, 4,  node.costs))  # Right
    nodes = [neighbor for neighbor in neighbors if neighbor.state is not None]
    heapList = []
    for node in nodes:
        if node not in closedList:
            heapq.heappush(heapList,node)
    return heapList


def move(state, operator):
    newState = np.copy(state)

    # Where findet index und gibt zurück (array([pos X]), array([pos Y])
    i = np.where(newState == 0)
    yPos = i[0][0]
    xPos = i[1][0]


    if operator == "Up":

        if yPos != 0:
        # Wenn ganz oben also X = 0 dann geht move nach oben nicht
            temp = newState[yPos-1][xPos]
            newState[yPos-1][xPos] = newState[yPos][xPos]
            newState[yPos][xPos] = temp

            return newState
        else:
            return None

    if operator == "Down":

        if yPos+1 != boardSide:

            temp = newState[yPos+1][xPos]
            newState[yPos+1][xPos] = newState[yPos][xPos]
            newState[yPos][xPos] = temp

            return newState
        else:
            return None

    if operator == "Left":
        if xPos != 0:

            temp = newState[yPos][xPos-1]
            newState[yPos][xPos-1] = newState[yPos][xPos]
            newState[yPos][xPos] = temp

            return newState
        else:
            return None

    if operator == "Right":
        if xPos+1 != boardSide:

            temp = newState[yPos][xPos +1]
            newState[yPos][xPos +1] = newState[yPos][xPos]
            newState[yPos][xPos] = temp
            
            return newState
        else:
            return None


def f(node):
    # h(f) + c(parent,node) + g(node)
    return distance(node)


def get_path_fom_node(node):
    # Pfad zur Lösung wird rückwärts erstellt.
    # Jede Node enthält einen Parent, somit gibt es bei gefundenem Ziel
    # eine einfach verkettete Liste vom Ziel zum Start
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

    start_time = time.time()
    heuristic = 'MANHATTAN'
    print("Starting A* with Manhatten")
    endNode = aStar()
    print("Found node")
    path = get_path_fom_node(endNode)
    print("Actual cost:", len(path))
    print("Solution path:", path)
    print("This took %s seconds" % (time.time() - start_time))
    print("---------------------------------")
    clear()

    start_time = time.time()
    heuristic = 'EUCLIDEAN'
    print("Starting A* with Euclidean")
    endNode = aStar()
    print("Found node")
    path = get_path_fom_node(endNode)
    print("Actual cost:", len(path))
    print("Solution path:", path)
    print("This took %s seconds" % (time.time() - start_time))