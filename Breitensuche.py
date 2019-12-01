from collections import deque


'''Einzelner zustand des Puzzles'''    
class Node:

    def __init__(self, state, parent, move, depth):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth # = cost
    
        if self.state:
            self.map = ''.join(str(e) for e in self.state)

goalNode = Node
operator = ["Up","Down", "Left", "Right"]  #Operatoren
start_state = [2, 8, 3, 1, 6, 4, 7, 0, 5]  #S
goal_state = [1, 2, 3, 8, 0, 4, 7, 6, 5]   #G 
 

puzzleLen = 0 #Puzzlegroesse
puzzleSize = 0 #Puzzle Seitenlaenge

searchDepth = 0


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

    raise Exception

'''Breitensuche'''
def bfs(start_state):
    queue =  deque([Node(start_state, None, None, 0)]) 
    search(queue, 'bfs')

        
'''Tiefensuche''' 
def dfs(start_state):
    stack =  list([Node(start_state, None, None, 0)]) # Erster Knoten in den Stack legen
    #Liste da die neu dazu Kommenden States auf den Stack gelegt werden sollen
    search(stack, "dfs")
    

'''Sucht alle Nachbarn eines Puzzlezustands '''
def findNeighbors(node):
    global operator
    
    neighbors = list()
    neighbors.append(Node(move(node.state, operator[0]), node, 1, node.depth + 1)) #Up
    neighbors.append(Node(move(node.state, operator[1]), node, 2, node.depth + 1)) #Down
    neighbors.append(Node(move(node.state, operator[2]), node, 3, node.depth + 1)) #Left
    neighbors.append(Node(move(node.state, operator[3]), node, 4, node.depth + 1)) #Right
    nodes = [neighbor for neighbor in neighbors if neighbor.state]
    
    return nodes

'''Erstellt einzelne Nachbarn eines Puzzlezustands'''
def move(state, operator):
    newState = state[:]

    i = newState.index(0) 
    if operator == "Up":
        if i not in range(0, puzzleSize): #prueft ob neighbor auserhalb des Puzzels liegt
            temp = newState[i - puzzleSize]
            newState[i - puzzleSize] = newState[i]
            newState[i] = temp
            return newState
        else:
            return None

    if operator == "Down": 
        if i not in range(puzzleLen - puzzleSize, puzzleLen):

            temp = newState[i + puzzleSize]
            newState[i + puzzleSize] = newState[i]
            newState[i] = temp

            return newState
        else:
            return None

    if operator == "Left":  
        if i not in range(0, puzzleLen, puzzleSize):

            temp = newState[i - 1]
            newState[i - 1] = newState[i]
            newState[i] = temp

            return newState
        else:
            return None

    if operator == "Right":  
        if i not in range(puzzleSize - 1, puzzleLen, puzzleSize):

            temp = newState[i + 1]
            newState[i + 1] = newState[i]
            newState[i] = temp
            return newState
        else:
            return None

''' Gibt eine Liste der Richtungen des kuerzesten Wegs zurueck'''
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

''' Gibt die Loesung des Puzzles aus'''
def printResult(search_methode):
    moves = moveDierection()
    print("Directions from "+ search_methode + ": " + str(moves) + "\n pfad costen: " + str(len(moves)))

''' Berechnet die Laenge und Seitenlaende des Puzzles '''
def puzzleSize():
    global puzzleLen, puzzleSize, start_state
    puzzleLen = len(start_state)
    puzzleSize = int(puzzleLen ** 0.5)
    
    
    
def main():
    puzzleSize()
    try:
        bfs(start_state)
        printResult("bfs")
        
        dfs(start_state)
        printResult("dfs")
    except:
        print("no solution")
        
    

if __name__ == '__main__':
    main()
        

