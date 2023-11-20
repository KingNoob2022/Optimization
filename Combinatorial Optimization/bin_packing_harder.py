# Import the libraries
from ortools.linear_solver import pywraplp


# Create Vehicle class and Order class
class Order:
    def __init__(self, quantity, cost):
        self.quantity = quantity
        self.cost = cost

    def __str__(self):
        return f"The order has quantity {self.quantity} and cost {self.cost}"


class Vehicle:
    def __init__(self, lower_capacity, upper_capacity):
        self.lower_capacity = lower_capacity
        self.upper_capacity = upper_capacity

    def __str__(self):
        return f"The truck has lower capacity: {self.lower_capacity} and upper capacity: {self.upper_capacity}"


# Get the data
num_of_orders, num_of_vehicles = -1, -1
orders = []
vehicles = []

read_data = open('medium_input_bin_data.txt')
count = 0
for line in read_data:
    if count == 0:
        num_of_orders, num_of_vehicles = tuple(map(int, line.split()))
        count += 1
    elif count <= num_of_orders:
        quantity, cost = tuple(map(int, line.split()))
        orders.append(Order(quantity, cost))
        count += 1
    else:
        lower_capacity, upper_capacity = tuple(map(int, line.split()))
        vehicles.append(Vehicle(lower_capacity, upper_capacity))


def create_data_model(order_list, vehicle_list):
    data = {}
    data['order'] = order_list
    data['items'] = list(range(len(order_list)))
    data['vehicle'] = vehicle_list
    data['bins'] = list(range(len(vehicle_list)))
    return data


# Declare the solver
solver = pywraplp.Solver.CreateSolver("SCIP")

# Create the variables
# x[i, j] = 1 if order i is served by vehicle j
data = create_data_model(orders, vehicles)
x = {}
for i in data['items']:
    for j in data['bins']:
        x[(i, j)] = solver.IntVar(0, 1, "x_%i_%i" %(i, j))

# Define the constraints
# Each order is served by at most one vehicle
for i in data['items']:
    solver.Add(sum([x[(i, j)] for j in data['bins']]) <= 1)

# Sum of quantity of orders served in a vehicle must be between the low capacity and up capacity
for j in data['bins']:
    solver.Add(sum([x[(i, j)] * orders[i].quantity for i in data['items']]) >= vehicles[j].lower_capacity)
    solver.Add(sum([x[(i, j)] * orders[i].quantity for i in data['items']]) <= vehicles[j].upper_capacity)

# Define the objective
# Maximize the total cost
solver.Maximize(solver.Sum([x[(i, j)] * orders[i].cost for i in data['items'] for j in data['bins']]))

# Call the solver and print the solution
status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    num_served_items = 0
    order_distribution = dict()
    for i in data['items']:
        for j in data['bins']:
            if x[(i, j)].solution_value() > 0:
                num_served_items += 1
                # print(f"Order {i + 1} is served by vehicle {j + 1}")
                if j + 1 not in order_distribution.keys():
                    order_distribution[j + 1] = [i + 1]
                else:
                    order_distribution[j + 1].append(i + 1)
    for key in order_distribution.keys():
        print(f"Truck {key} takes orders: {order_distribution[key]}")
    print(f"Total orders served: {num_served_items}")
    print(f"Total cost:", solver.Objective().Value())
    print("Time = ", solver.WallTime(), "milliseconds")
else:
    print("The problem does not have an optimal solution")

'''-------------------Experimentation Note---------------------'''
# input size = 300 => Time = 1539 milliseconds
# input size >= 500 => Long Execution Time => Implement Greedy Algorithms/ Heuristic Algorithm
