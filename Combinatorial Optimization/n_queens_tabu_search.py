import random
import time

# Start timer
start_time = time.time()

# Define the objective function


def objective_function(solution):
    # TODO: Implement your objective function here
    # The objective function should evaluate
    # the quality of a given solution and
    # return a numerical value representing
    # the solution's fitness
    # Example: return sum(solution)
    # return sum(solution)
    result_sum = 0
    n = len(solution)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(solution[i] - solution[j]) == j - i:
                result_sum += 1
    return result_sum



# Define the neighborhood function


def get_neighbors(solution):
    # TODO: Implement your neighborhood function here
    # The neighborhood function should generate
    # a set of neighboring solutions based on a given solution
    # Example: Generate neighboring solutions by
    # swapping two elements in the solution

    neighbors = {}
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbor = solution[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors[neighbor[i], neighbor[j]] = neighbor
    return neighbors


# Define the Tabu Search algorithm


def tabu_search(initial_solution, max_iterations, tabu_list_size, avoid_times):
    best_solution = initial_solution
    current_solution = initial_solution
    aspiration_level = float('inf')
    # count = 0
    step = 0
    tabu_list = []

    for _ in range(max_iterations):
        step += 1
        neighbors = get_neighbors(current_solution)
        best_neighbor = None
        best_neighbor_key = None
        best_neighbor_fitness = float('inf')

        for key in neighbors:
            x = objective_function(neighbors[key])
            if x < aspiration_level:
                aspiration_level = x
                best_neighbor = neighbors[key]
                best_neighbor_key = key
                for j in range(avoid_times):
                    tabu_list.append(key)
                break
            if key not in tabu_list:
                neighbor_fitness = x
                if neighbor_fitness < best_neighbor_fitness:
                    best_neighbor = neighbors[key]
                    best_neighbor_key = key
                    best_neighbor_fitness = neighbor_fitness

        if best_neighbor is None:
            # No non-tabu neighbors found,
            # terminate the search
            break

        current_solution = best_neighbor
        for j in range(avoid_times):
            tabu_list.append(best_neighbor_key)
        tabu_list.pop(0)
        if len(tabu_list) > tabu_list_size:
            # Remove the oldest entry from the
            # tabu list if it exceeds the size
            tabu_list.pop(0)

        if objective_function(best_neighbor) < objective_function(best_solution):
            # Update the best solution if the
            # current neighbor is better
            best_solution = best_neighbor
        #     count = 0
        #
        # if objective_function(best_neighbor) == objective_function(best_solution):
        #     count += 1
        #
        # if count == 3:
        #     break

    print("Found at Step:", step)
    return best_solution


# Example usage
# Provide an initial solution
table_size = int(input("Enter the table size: "))
initial_solution = [i for i in range(table_size)]
max_iterations = 500
tabu_list_size = 10

best_solution = tabu_search(initial_solution, max_iterations, tabu_list_size, 4)
print("Best solution: {}".format(best_solution))
print("Best solution fitness: {}".format(objective_function(best_solution)))


# End timer
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)