'''
aviv shisman
206558157
'''

from queue import PriorityQueue


inputFileName='tests/input2.txt'


#globals for IDS
Visited=[]
currentDepth=0
IDSCount=0
limit=0
startState=None

#for Astar
timeDev=0

'''
Main
'''
def main():
    print ("Welcome to my solver, I will now read you file and produce the output for you")
    readAndStart()

'''
Read input file
'''
def readAndStart():
    #getting input
    inputFile=open(inputFileName,'r')
    algorithem=int(inputFile.readline().rstrip('\n'))
    size=int(inputFile.readline().rstrip('\n'))
    startState=inputFile.readline().rstrip('\n').split('-')

    #getting board and openSpot on board
    board,openIndex=translateToBoard(startState,size)


    print (startState)
    #activate the solver of choice
    if algorithem==1:
        IDS(board,size,openIndex)
    elif algorithem==2:
        BFS(board,size,openIndex)
    else:
        AStar(board,size,openIndex)

    return

'''
BFS like we learned in class,getting next node from open list and check goal state
'''
def BFS(board,size,openSpot):
    #check start state
    if goalState(board,size):
        results('start', 0, 0)
        print ('BFS Finished :)')
        return

    #start of BFS:
    print ('BFS Start:\n')
    openList=BFSSearch(board, size, openSpot, '')
    start=next(iter(openList), None)
    start.prev='none' #req for class
    nextNode=Node(next(iter(openList), None))
    openCount=1

    #BFS loop, get next elm then search by bfs
    while nextNode!=None:
        openCount += 1
        nextNode.applyMove()
        nextNode.route=str(nextNode.route)+str(nextNode.getDirection())
        if(nextNode.route=='DLUULDDRRUUL'):
            print('yes')
        if goalState(nextNode.state,nextNode.size):
            results(nextNode.route,openCount,0)
            print (nextNode.route+' '+str(openCount)+' 0')
            print ('BFS Finished :)')
            return
        openList.extend(BFSSearch(nextNode.state, size, nextNode.freeIndex, nextNode.route))
        del openList[0]
        temp=next(iter(openList), None)
        temp.prev='none'
        nextNode = Node(temp)

'''
Check for all possible moves in current position and add them by BFS Reasoning
'''
def BFSSearch(board, size, openSpot, route):
    moves=[]
    i,j=openSpot
    #if there are rows below him, then moving up is possible
    if i<size-1:
        moves.append(Node(None,'U',copyBoard(board,size),(i,j),(i+1,j),size,route))
    #if there are rows above him,then moving down is possible
    if i>0:
        moves.append(Node(None,'D',copyBoard(board,size),(i,j),(i-1,j),size,route))
    # if there are rows in the right side of him moving left is possible
    if j < size - 1:
        moves.append(Node(None,'L',copyBoard(board,size),(i,j),(i,j+1),size,route))
    # if there are rows in the left side of him moving right is possible
    if j > 0:
        moves.append(Node(None,'R',copyBoard(board,size),(i,j),(i,j-1),size,route))

    return moves

'''
IDS, searching by IDS and incrementing the limit everytime we tried all possible options(like the algorithm).
notice that here i only get next node and check for goal state.
in IDS search i get the next node by IDS reasoning + i change the limit when needed
'''
def IDS(board,size,openSpot):
    print ('IDS Start:\n')

    #check start state
    Visited.append(board)
    if goalState(board,size):
        results('start',0, 0)
        print ('IDS Finished :)')
        return

    #start of IDS setting the algorithm
    start=Node(None,'',copyBoard(board,size),openSpot,'',size,'')
    start.setPrev('start')
    global limit
    global startState
    global IDSCount
    IDSCount=1 #we visited first elm
    limit=1                                                 #limit of depth
    startState=Node(start)                                  #start state is global
    openList=IDSSearch(start,board, size, openSpot, '')     #get next elm by IDS Search
    nextNode=Node(next(iter(openList), None))

    #the main loop get the next node and check him everytime while using IDS search
    while nextNode!=None:
        nextNode.route=str(nextNode.route)+str(nextNode.getDirection())
        if goalState(nextNode.state,nextNode.size):
            global currentDepth
            results(nextNode.route,IDSCount,currentDepth)
            print (nextNode.route+' '+str(IDSCount)+' '+str(currentDepth))
            print ('IDS Finished :)')
            return
        openList.extend(IDSSearch(nextNode,nextNode.state, size, nextNode.freeIndex, nextNode.route))
        openList.remove(openList[0])
        nextNode = Node(next(iter(openList), None))
    return

'''
implement IDS logic and search the next element in graph by it + changing limit when needed
'''
def IDSSearch(current,board, size, openSpot, route):
    moves=[]
    i,j=openSpot
    global currentDepth
    global limit
    global IDSCount
    prevNode=current

    #if there are rows below him, then moving up is possible
    if i<size-1 and currentDepth<limit:
        nextNode=Node(None,'U',copyBoard(board,size),(i,j),(i+1,j),size,route)
        nextNode.applyMove()
        if checkVisited(nextNode.state,size) == False:
            currentDepth += 1
            IDSCount+=1
            nextNode.prev=prevNode
            current=nextNode
            Visited.append(nextNode.state)
            moves.append(nextNode)
            return moves

    #if there are rows above him,then moving down is possible
    if i>0 and currentDepth<limit:
        nextNode=Node(None,'D',copyBoard(board,size),(i,j),(i-1,j),size,route)
        nextNode.applyMove()
        if checkVisited(nextNode.state, size) == False:
            currentDepth += 1
            IDSCount+=1
            nextNode.prev=prevNode
            current=nextNode
            Visited.append(nextNode.state)
            moves.append(nextNode)
            return moves

    # if there are rows in the right side of him moving left is possible
    if j < size - 1 and currentDepth<limit:
        nextNode=Node(None,'L',copyBoard(board,size),(i,j),(i,j+1),size,route)
        nextNode.applyMove()
        if checkVisited(nextNode.state, size) == False:
            currentDepth += 1
            IDSCount+=1
            nextNode.prev=prevNode
            current=nextNode
            Visited.append(nextNode.state)
            moves.append(nextNode)
            return moves

    # if there are rows in the left side of him moving right is possible
    if j > 0 and currentDepth<limit:
        nextNode=Node(None,'R',copyBoard(board,size),(i,j),(i,j-1),size,route)
        nextNode.applyMove()
        if checkVisited(nextNode.state, size) == False:
            currentDepth += 1
            IDSCount+=1
            nextNode.prev=prevNode
            current=nextNode
            Visited.append(nextNode.state)
            moves.append(nextNode)
            return moves

    if len(moves)==0:

        #If true: we got to limit and check all possible options so->limit++ and start over
        if currentDepth==0: #need to start over with higher limit
            limit+=1
            #clean memory
            del Visited[:]
            global startState
            IDSCount+=1 #reset Count
            newStart=Node(startState) #get StartState and start over
            Visited.append(newStart.state)
            return IDSSearch(newStart,newStart.state, size,newStart.freeIndex, '')

        #we checked possiblity and no more or limit so return back to check if there are other possiblities
        #in depth-=1
        else:
            current=Node(current.prev)
            currentDepth=currentDepth-1
            return IDSSearch(current,current.state,size,current.freeIndex,current.route)

'''
AStar, searching by AStart logic for next element.
notice that here i only get next node and check for goal state.
'''
def AStar(board,size,openSpot):
    # check start state
    if goalState(board, size):
        results('start', 0, 0)
        print('AStar finished :)')
        return

    # start of AStar:
    print('AStar Start:\n')
    #start of IDS setting the algorithm
    start=Node(None,'',copyBoard(board,size),openSpot,'',size,'')
    start.setPrev('start')
    start.setDepth(0)
    start.setFval(calcF(board, size, 0))
    startState=Node(start)
    startState.setTimeDev(0)
    openList = PriorityQueue()
    openList.put(startState)


    openCount = 0
    flag=1

    # AStar loop
    while flag==1:
        openCount += 1
        temp = openList.get()
        nextNode = Node(temp)
        nextNode.route = str(nextNode.route) + str(nextNode.getDirection())
        if goalState(nextNode.state, nextNode.size):
            results(nextNode.route, openCount,len(nextNode.route))
            print(nextNode.route + ' ' + str(openCount) + ' '+str(len(nextNode.route)))
            print('AStar Finished')
            flag=0
            return
        openList=AStarSearch(openList,nextNode,nextNode.state, size, nextNode.freeIndex,
                                    nextNode.route,nextNode.getDepth())

    return


'''
Help function for AStar that find the next node
'''
def AStarSearch(moves,current,board, size, openSpot, route,depth):

    i, j = openSpot
    global timeDev

    # if there are rows below him, then moving up is possible
    if i < size - 1:
        next=Node(None, 'U', copyBoard(board, size), (i, j), (i + 1, j), size, route)
        next.applyMove()
        next.setDepth(depth + 1)
        next.prev = current
        next.setTimeDev(timeDev)
        timeDev += 1
        Fval = calcF(next.state, size, depth + 1)
        next.setFval(Fval)
        moves.put(next)

    # if there are rows above him,then moving down is possible
    if i > 0:
        next=Node(None, 'D', copyBoard(board, size), (i, j), (i - 1, j), size, route)
        next.applyMove()
        next.setDepth(depth+1)
        next.prev=current
        next.setTimeDev(timeDev)
        timeDev+=1
        Fval=calcF(next.state,size,depth+1)
        next.setFval(Fval)
        moves.put(next)

    # if there are rows in the right side of him moving left is possible
    if j < size - 1:
        next=Node(None, 'L', copyBoard(board, size), (i, j), (i, j + 1), size, route)
        next.applyMove()
        next.setDepth(depth + 1)
        next.prev = current
        next.setTimeDev(timeDev)
        timeDev += 1
        Fval = calcF(next.state, size, depth + 1)
        next.setFval(Fval)
        moves.put(next)

    # if there are rows in the left side of him moving right is possible
    if j > 0:
        next=Node(None, 'R', copyBoard(board, size), (i, j), (i, j - 1), size, route)
        next.applyMove()
        next.setDepth(depth + 1)
        next.prev = current
        next.setTimeDev(timeDev)
        timeDev += 1
        Fval = calcF(next.state, size, depth + 1)
        next.setFval(Fval)
        moves.put(next)

    return moves



'''
calc F Value (g()+h())
'''
def calcF(board,size,gVal):
    return gVal+calcHeuristic(board,size)


'''
manhattan sum 
'''
def calcHeuristic(board, size):
    sum=0
    k=0
    end=size-1
    for i in range(size):
        for j in range(size):
            if board[i][j]!=0:
                list2=list(sorted(toVec(board,size)))
                list2.remove(list2[0])
                list2.append(0)
                temp,idx=translateToBoard(list2,size)
                i2,j2=index_2d(temp,board[i][j],size)
                diff1=abs(i2-i)
                diff2=abs(j2-j)
                sum+=diff1+diff2


    return sum

'''
Help function
'''
def index_2d(myList, v,size):
    for i in range (size):
        for j in range(size):
            if v==myList[i][j]:
                return i,j

'''
Help function, check if we visited certin state
'''
def checkVisited(state,size):
    for k in range(len(Visited)):
        current=Visited[k]
        if checkEqual(state,current,size)==True:
            return True
    return False

'''
check if states are equal
'''
def checkEqual(state,current,size):
    for i in range(size):
        for j in range(size):
            if current[i][j] != state[i][j]:
                return False
    return True

'''
write results to file
'''
def results(route,openCount,costOrDepth):
    outputName='output.txt'
    output=open(outputName,'w')
    output.write(route+' '+str(openCount)+' '+str(costOrDepth)+'\n')

    return

'''
Translate board to array[][]
'''
def translateToBoard(mylist,size):
    board=[[0 for x in range(size)] for y in range(size)]
    c=0
    spotIndex=0
    for i in range (size):
        for j in range(size):
            board[i][j]=int(mylist[c])
            c+=1
            if board[i][j]==0:
                spotIndex=(i,j)

    return board,spotIndex

'''
Check if Goal
'''
def goalState(board,size):
    if board[size-1][size-1]==0:
        vec=toVec(board,size)
        for i in range(len(vec)-2):
            if vec[i]>vec[i+1]:
                return False
        return True
    return False

'''
turning board(arr) to vector
'''
def toVec(board,size):
    vec=[]
    for i in range(size):
        for j in range(size):
            vec.append(board[i][j])
    return vec

'''
Copy Board
'''
def copyBoard(board, size):
    copy = [[0 for x in range(size)] for y in range(size)]
    for i in range(size):
        for j in range(size):
            copy[i][j] = board[i][j]

    return copy

'''
The Node Class
'''

'''
Node class!
'''
class Node:

    def __init__(self,NodeA,Direction='', state='', freeIndex='', swapIndex='',size=0,route=''):
        if NodeA!=None:
            self.Direction = NodeA.Direction
            self.freeIndex = NodeA.freeIndex
            self.swapIndex = NodeA.swapIndex
            self.state = NodeA.state
            self.route=NodeA.route
            self.size=NodeA.size
            self.prev=NodeA.prev
            self.depth=NodeA.getDepth()
            if NodeA.getFval()!=-1:
                self.fVal=NodeA.fVal

        else:
            self.Direction = Direction
            self.freeIndex = freeIndex
            self.swapIndex = swapIndex
            self.state = state
            self.route=route
            self.size=size
            self.depth=0



    def applyMove(self):
        #swap open spot with possible move
        arr=self.state
        i1,j1=self.swapIndex
        i2,j2=self.freeIndex
        temp=arr[i1][j1]
        self.state[i1][j1]=arr[i2][j2]
        self.state[i2][j2]=temp

        #update new open spot
        self.freeIndex=(i1,j1)

        return

    def getDirection(self):
        return self.Direction

    def getFreeIndex(self):
        return self.freeIndex

    def getSwapIndex(self):
        return self.swapIndex

    def getState(self):
        return self.state

    def setPrev(self,prev):
        self.prev=prev

    def setDepth(self,d):
        self.depth=d

    def setFval(self,v):
        self.fVal=v

    def getDepth(self):
        try:
            return self.depth
        except AttributeError:
            return -1

    def getFval(self):
        try:
            return self.fVal
        except AttributeError:
            return -1

    def __lt__(self, other):
        #try order by F value, if equal try by depth
        if self.fVal==other.fVal:
            #try order by depth if equal try by direction(up,down..)
            if self.getDepth()==other.getDepth():
                return self.getDirectionValue()<other.getDirectionValue()
            else:
                return self.getDepth()<other.getDepth()

        else:
            return self.fVal<other.fVal


    def setTimeDev(self,v):
        self.time=v

    def getDirectionValue(self):
        if self.Direction=='U':
            return 1
        if self.Direction=='D':
            return 2
        if self.Direction=='L':
            return 3
        if self.Direction=='R':
            return 4




if __name__ == "__main__":
    main()
