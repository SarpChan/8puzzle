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

    def __str__(self):
        return "state:\n %s,\n costs: %i" % (self.state,self.costs)

    def __lt__(self, other):
        return self.costs, other.costs

def aStart():
    openList = []
    closedList = []

    root = Node(START, None, None, 0, 0)
    test = Node(GOAL, root, "down", 1, 0)
    heapq.heappush(openList,root)
    heapq.heappush(openList,test)
    while openList:
        next_item = heapq.heappop(openList)
        print(next_item)


if __name__ == "__main__":
    aStart()