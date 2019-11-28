from collections import deque


operator = ["Up","Down", "Left", "Right"]  #Operatoren
start_state = [2, 8, 3, 1, 6, 4, 7, 0, 5]  #S
goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]   #G 
 


#puzzle Size
puzzleLen = 0
boardSide = 0

searchDepth = 0

'''Einzelner zustand'''    
class State:

    def __init__(self, state, parent, move, depth):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth # = cost
    
        if self.state:
            self.map = ''.join(str(e) for e in self.state)

goalNode = State

def search(queue,searchmethode):
    global goalNode, searchDepth  
    explored = set ()
   
    while queue:
        if searchmethode == "dfs":
            node = queue.pop()
        else :
            node = queue.popleft()
        
        explored.add(node.map)

        if node.state == goal_state:
            goalNode = node
            return queue
        
        if searchmethode == "dfs":
            neighbors = reversed(findNeighbors(node))
        else :
            neighbors = findNeighbors(node) #Nachfolger des Knotens
        

        for neighbor in neighbors:
            if neighbor.map not in explored:
                queue.append(neighbor)
                explored.add(neighbor.map)

                if neighbor.depth > searchDepth:
                    searchDepth += 1   



'''Breitensuche'''
def bfs(start_state):
    queue =  deque([State(start_state, None, None, 0)]) # Start State, parent, move, key,depth,cost , 
    search(queue, 'bfs')

        
'''Tiefensuche''' 
def dfs(start_state):
    stack =  list([State(start_state, None, None, 0)]) # Erster Knoten in den Stack legen
    #Liste da die neu dazu Kommenden States auf den Stack gelegt werden sollen
    search(stack, "dfs")
    


def findNeighbors(node):
    global operator
    
    neighbors = list()
    neighbors.append(State(move(node.state, operator[0]), node, 1, node.depth + 1)) #Up
    neighbors.append(State(move(node.state, operator[1]), node, 2, node.depth + 1)) #Down
    neighbors.append(State(move(node.state, operator[2]), node, 3, node.depth + 1)) #Left
    neighbors.append(State(move(node.state, operator[3]), node, 4, node.depth + 1)) #Right
    nodes = [neighbor for neighbor in neighbors if neighbor.state]
    
    return nodes


def move(state, operator):
    newState = state[:]

    i = newState.index(0)

    if operator == "Up":

        if i not in range(0, boardSide):

            temp = newState[i - boardSide]
            newState[i - boardSide] = newState[i]
            newState[i] = temp

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
        if i not in range(0, puzzleLen, boardSide):

            temp = newState[i - 1]
            newState[i - 1] = newState[i]
            newState[i] = temp

            return newState
        else:
            return None

    if operator == "Right":  
        if i not in range(boardSide - 1, puzzleLen, boardSide):

            temp = newState[i + 1]
            newState[i + 1] = newState[i]
            newState[i] = temp
            return newState
        else:
            return None


def moveDierection():
    currentNode = goalNode
    moves = list()
    while start_state != currentNode.state:

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


def printResult(search_methode):
    moves = moveDierection()
    print("directions from "+ search_methode + ": " + str(moves) + "\n pfad costen: " + str(len(moves)))


def puzzleSize():
    global puzzleLen, boardSide, start_state
    puzzleLen = len(start_state)
    boardSide = int(puzzleLen ** 0.5)
    
    
    
def main():
    puzzleSize()
    
    bfs(start_state)
    printResult("bfs")
    
    dfs(start_state)
    printResult("dfs")
    

if __name__ == '__main__':
    main()
        

