import time

# Start timer
start_time = time.time()

# Read the input data
num_cities = int(input())
route_matrix = []
read_data = open('data.txt')
for line in read_data:
    data = list(map(int, line.split()))
    route_matrix.append(data)

# Get the input
# for i in range(num_cities):
#     temp = list(map(int, input().split()))
#     route_matrix.append(temp)
# print(route_matrix)


# Import the libraries
from ortools.linear_solver import pywraplp

# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver("SCIP")

if not solver:
    print("Can't solve")

# x[i, j] is an array of 0-1 variables, which will be 1
# if worker i is assigned to task j.
x = {}
for i in range(num_cities):
    for j in range(num_cities):
        x[i, j] = solver.IntVar(0, 1, "")

# Each worker is assigned to at most 1 task.
for i in range(num_cities):
    solver.Add(solver.Sum([x[i, j] for j in range(num_cities) if i != j]) == 1)

# Each task is assigned to exactly one worker.
for j in range(num_cities):
    solver.Add(solver.Sum([x[i, j] for i in range(num_cities) if i != j]) == 1)

array_input = [i for i in range(1, num_cities + 1)]

''' 
### Backtracking to generate all the subsets of a list
def TRY(i, k, subset, res, list_length):
    for v in range(subset[i - 1] + 1, list_length - k + i + 1):
        temp = subset.copy()
        temp.append(v)
        if i == k:
            res.append(tuple(temp[1:]))
        else:
            TRY(i + 1, k, temp, res, list_length)

all_subset = []
for i in range(2, num_cities):
    temp = []
    TRY(1, i, [0], temp, num_cities)
    all_subset.append(temp)
'''

has_found_sol = False
k = num_cities - 1


def create_pair(l, num_var):
    k = len(l)
    new_temp = []
    if num_var >= 80:
        for i in range(k - 1):
            for j in range(i + 1, k):
                new_temp.append((l[i], l[j]))
                new_temp.append((l[j], l[i]))
    else:
        for i in range(k - 1):
            new_temp.append((l[i], l[i + 1]))
    return new_temp


while not has_found_sol:
    # temp = all_subset[k - 2]
    # for l in temp:
    #     new_temp = []
    #     for i in range(k - 1):
    #         for j in range(i + 1, k):
    #             new_temp.append((l[i], l[j]))
    #             new_temp.append((l[j], l[i]))
    #     solver.Add(solver.Sum([x[i - 1, j - 1] for (i, j) in new_temp]) <= k - 1)

    objective_terms = []
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                objective_terms.append(route_matrix[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        # print(f"Total cost = {solver.Objective().Value()}\n")
        path_list = []
        for i in range(num_cities):
            for j in range(num_cities):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if x[i, j].solution_value() > 0.5:
                    path_list.append((j + 1, i + 1))
                    # print(f"Worker {j + 1} assigned to task {i + 1}." + f" Cost: {route_matrix[i][j]}")

        # Display the resulting routes
        result = [1]
        check = True
        while check:
            for i in path_list:
                if result[-1] == i[0]:
                    if i[1] not in result:
                        result.append(i[1])
                    else:
                        check = False
                        break
        if len(result) == num_cities:
            print(num_cities)
            print(*result)
            print(f"Total cost = {solver.Objective().Value()}\n")
            has_found_sol = True
        else:
            result.append(1)
            # Add more sub-tour elimination constraints if the result doesn't satisfy the constraint of the problem
            solver.Add(solver.Sum([x[j - 1, i - 1] for (i, j) in create_pair(result, num_cities)]) <= len(result) - 2)
if not has_found_sol:
    print("No solution found.")

# End timer
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)
