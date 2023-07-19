import copy

class State:
    def __init__(self, size: int, matrix: list[list], row: list, col: list, prev = None):
        self.size = size
        self.matrix = copy.deepcopy(matrix)
        self.row = row
        self.col = col
        self.tents_placed = len(getAllTentPosition(self))
        self.prev = prev
        # For A-Star Algorithm
        self.trees_uncovered = getUncoveredTrees(self)
        self.cells_empty = getEmptyCells(self)
        self.cost = cost_function(self)
        
    def __eq__(self, __other: object) -> bool:
        if isinstance(__other, State):
            for i in range(self.size):
                for j in range(self.size):
                    if self.matrix[i][j] != __other.matrix[i][j]: return False
            return True
        return False
    
    def __lt__(self,__other)-> bool:
        if isinstance(__other, State):
            return self.cost < __other.cost
        return False
            
# ! Rule Function: 

#Get list posistion of all tree in the matrix (New)
def getAllTreePosition(state:State):
   res = []
   for i in range(state.size):
      for j in range (state.size):
         if state.matrix[i][j] == 1:
            res.append([i,j])
   return res

#Get list position of tents pitched in the matrix (New)
def getAllTentPosition(state:State):
   res = []
   for i in range(state.size):
      for j in range (state.size):
         if state.matrix[i][j] == 2:
            res.append([i,j])
   return res

def handlePosition(x, y, state: State):
    max = state.size
    #print(f"x: {x}, y: {y}, max: {max}")
    if x < 0 or x >= max or y < 0 or y >= max: return False
    else: return True

# Return a list of position[x,y] just above, below, right, left that position 1 unit
def getHorAndVerMoves(point: list, state: State):
    res = []
    if handlePosition(point[0]-1, point[1], state): res.append([point[0]-1, point[1]])
    if handlePosition(point[0]+1, point[1], state): res.append([point[0]+1, point[1]])
    if handlePosition(point[0], point[1]-1, state): res.append([point[0], point[1]-1])
    if handlePosition(point[0], point[1]+1, state): res.append([point[0], point[1]+1])
    return res

def getDiagonalMoves(point: list, state: State):
    res = []
    if handlePosition(point[0]-1, point[1]-1, state): res.append([point[0]-1, point[1]-1])
    if handlePosition(point[0]-1, point[1]+1, state): res.append([point[0]-1, point[1]+1])
    if handlePosition(point[0]+1, point[1]-1, state): res.append([point[0]+1, point[1]-1])
    if handlePosition(point[0]+1, point[1]+1, state): res.append([point[0]+1, point[1]+1])
    return res

# Return a list of position[x,y] around that position
def getAllLegalMoves(point: list, state: State):
    return getHorAndVerMoves(point, state) + getDiagonalMoves(point, state)

# Check if this position is valid to put a tent(2) in
def isValidPostion(point: list, state: State):
    x = point[0]
    y = point[1]
    if (state.matrix[x][y]) == 0: # check if that position is empty
        # check if at least 1 tent exists around the position
        allMoves = getAllLegalMoves(point, state) 
        for ele in allMoves:
            i = ele[0]
            j = ele[1]
            if state.matrix[i][j] == 2: return False  
        # check if at least 1 tree is around the position
        allVerAndFor = getHorAndVerMoves(point, state)
        for cursor in allVerAndFor:
            i = cursor[0]
            j = cursor[1]
            # print(f"i: {i}, j: {j}")
            if state.matrix[i][j] == 1: return True
        return False
    else: return False

# Check if the number of tents in our position's row and column has exceeded the allowed amount
def isOverAvailableTents(point: list, state: State):
    if not(isValidPostion(point, state)): return False
    else:
        cnt_row = 0
        cnt_col = 0
        point_row = point[0]
        point_col = point[1]
        # count how many tents have put in that position'row and column
        for i in range(state.size):
            if state.matrix[point_row][i] == 2: cnt_row += 1
        if cnt_row >= state.row[point_row]: return False
        # check if the number of tents is greater or equal the allowed amount
        for j in range(state.size):
            if state.matrix[j][point_col] == 2: cnt_col += 1
        if cnt_col >= state.col[point_col]: return False
        return True

def canPutTent(point: list, state: State):
    if isValidPostion(point, state) and isOverAvailableTents(point, state):
        return True
    else: return False
    
def isBFSGoalState(state: State):
    sum = 0
    for i in state.row:
        sum += i
    #print(f"state.getTents: {state.tents_placed}\nsum: {sum}")
    if state.tents_placed == sum: return True
    else: return False

def genNextStatesList(state: State):
    res = []
    for i in range(state.size):
        for j in range(state.size):
            if canPutTent([i,j], state):
                temp = State(state.size, copy.deepcopy(state.matrix), state.row, state.col, state)
                temp.matrix[i][j] = 2
                temp.tents_placed = state.tents_placed + 1
                temp.trees_uncovered = state.trees_uncovered -1 #when call State(), it also calls self.trees_uncovered = getUncoveredTrees(self)?
                # temp.cells_empty = getEmptyCells(temp) #when call State(), it also calls self.cells_empty = getEmptyCells(self)?
                temp.cost = cost_function(temp)
                res.append(temp)
    return res

# ! For A-Star Algorithm: 
def cost_function(state: State):
    # """Duy's h(n)"""
    failed_tree_canNotPitch = getUnPitchableTree(state)
    value = 0
    for i in range(state.size): 
        if state.row[i] == 0:
            continue
        else:
            remainClue = countRemainClueOfRow(i,state)
            remainCanPutTent = countRemainCanPutTentForRow(i,state)
            if remainClue == 0:
                value-=2
                continue
            else:
                if remainClue > remainCanPutTent:
                    value +=10
                else:
                    value += (remainCanPutTent - remainClue)*0.2
                    if remainClue == remainCanPutTent:
                        value+=3*remainClue
    for j in range(state.size): 
        if state.col[j] == 0: 
            continue
        else:
            remainClue = countRemainClueOfCol(j,state)
            remainCanPutTent = countRemainCanPutTentForCol(j,state)
            if remainClue == 0:
                value-=2
                continue
            else:
                if remainClue > remainCanPutTent:
                    value +=10
                # elif remainClue == remainCanPutTent:
                #     value += 3*remainClue
    return value + failed_tree_canNotPitch*5 # cost is prior to level that finish the clue of each row and col

def getEmptyCells(state: State):
    cnt = 0
    for i in range(state.size):
        for j in range(state.size):
            if state.matrix[i][j] == 0: cnt += 1
    return cnt

#count qty of can-put-tent position of a Row
def countRemainCanPutTentForRow(i: int, state:State):
    count = 0
    for j in range(state.size):
        if state.matrix[i][j] == 1 or state.matrix[i][j] == 2:
            continue
        if canPutTent([i,j],state):
            count +=1
    return count

#count qty of can-put-tent position of a Col
def countRemainCanPutTentForCol(j: int, state:State):
    count = 0
    for i in range(state.size):
        if state.matrix[i][j] == 1 or state.matrix[i][j] == 2:
            continue
        if canPutTent([i,j],state):
            count +=1
    return count
    
#count qty of remaining allowable clue of the row    
def countRemainClueOfRow(i: int, state:State):
    count = state.row[i]
    for j in range(state.size):
        if state.matrix[i][j] == 2:
            count-=1
    return count

#count qty of remaining allowable clue of the row    
def countRemainClueOfCol(j: int, state:State):
    count = state.col[j]
    for i in range(state.size):
        if state.matrix[i][j] == 2:
            count-=1
    return count

def isFailedTree(posCheck:list, state:State): #failedTree is the tree that is not pitched the tent besides and has no canputTent position
    list_canPitchTent = getHorAndVerMoves(posCheck,state)
    for pos in list_canPitchTent:
        if state.matrix[pos[0]][pos[1]] == 2:
            return False
        if canPutTent(pos, state):
            return False
    return True

def getUnPitchableTree(state:State):
    a = 0
    listTree = getAllTreePosition(state)
    for Tree in listTree:
        if isFailedTree(Tree,state):
            a += 1
    return a

def getUncoveredTrees(state: State):
    #note: count the number of tree then sub tents pitched count
    listTrees = getAllTreePosition(state)
    qtyTrees = len(listTrees)
    return qtyTrees - state.tents_placed

def isAStarGoalState(state: State):
    return state.trees_uncovered == 0

def getSubMatrix(state1: State, state2: State):
    result = []
    for i in range(state1.size):
        row = []
        for j in range(state1.size):
            row.append(state1.matrix[i][j] - state2.matrix[i][j])
        result.append(row)
    return result