import random
import time

# Start timer
start_time = time.time()

def Violation():
    # return the number of violation
    v = 0
    for i in range (n - 1):
        for j in range (i + 1, n):
            if x[i] == x[j]: # i and j on the same row
                v += 1
            if x[i] + i == x[j] + j: # i and j are on the same diagonal
                v += 1
            if x[i] - i == x[j] - j: # i and j are on the same diagonal
                v += 1
    return v

def Violation_of_queen(q):
    # return the number of vioaltions of queen q
    v = 0
    for i in range (n):
        if i != q: 
            if x[i] == x[q]: # same row
                v += 1
            if x[i] + i == x[q] + q: 
                v += 1
            if x[i] - i == x[q] - q:
                v += 1
    return v

def Select_most_Violating_queen():
    MaxViolation = 0
    select_queen = -1
    candidate = []
    for q in range (n):
        v = Violation_of_queen(q)
        if v > MaxViolation:
            MaxViolation = v
            candidate = []
            candidate.append(q)
        elif v == MaxViolation: candidate.append(q)
    i = random.randint(0, len(candidate) - 1)
    select_queen = candidate[i]
    return select_queen

def GetDelta(q, r):
    # return the change of the mnumber of violation if queen q is moved to row r
    current_row = x[q]
    x[q] = r
    new_violation = Violation() 
    delta = new_violation - violation
    x[q] = current_row # retore current route
    return new_violation - violation

def Select_most_Promise_row(q):
    min_delta = 9999999999999
    selected_row = -1
    candidate = []
    for r in range (n):
        delta = GetDelta(q, r) # move queen q to row r
        if delta < min_delta:
            min_delta = delta
            candidate = []
            candidate.append(r)
        elif delta == min_delta:
            candidate.append(r)
    i = random.randint(0, len(candidate) - 1)
    selected_row = candidate[i]
    return selected_row

def print_board(board):
    for i in range (n):
        board[i][x[i]] = 1
    for row in range (n):
        for col in range (n):
            if board[row][col] == 1: print("♕", end = ' ')
            else: print("☐", end = ' ')
        print()

def Local_Search_Max_Iteration(maxIter):
    for it in range (maxIter):
        q = Select_most_Violating_queen()
        r = Select_most_Promise_row(q)
        x[q] = r
        violation = Violation()
        # print("step: ", it, "violation = ", violation)
        if Violation() == 0:
            print("FOUND at step: ", it)
            print_board(board)
            break

n = 200
x = [0 for i in range (n)] # current sol x[i] is the row of queen i
board = [[0 for i in range (n)] for j in range (n)]
violation = Violation() # store cur violation of queen i-th

Local_Search_Max_Iteration(10000)

# End timer
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)
