# Read the input data
num_cities = int(input())

cost_matrix = []
read_data = open('data.txt')
for line in read_data:
    data = list(map(int, line.split()))
    cost_matrix.append(data)

n = len(cost_matrix)

# Import the library
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

# Model
model = pyo.ConcreteModel()  # ConcreteModel() creates the model

# Indexes for the cities
model.M = pyo.RangeSet(n)  # RangeSet(n) creates an index from 1 to n
model.N = pyo.RangeSet(n)

# Index for the dummy variable u
model.U = pyo.RangeSet(2, n)  # RangeSet(2, n) creates an index from 2 to n

print(pyo.RangeSet(2, n))

# Decision variables xij
model.x = pyo.Var(model.N, model.M, within=pyo.Binary)  # creates n x m decision variables xij

# Dummy variable ui
model.u = pyo.Var(model.N, within=pyo.NonNegativeIntegers, bounds=(0, n - 1))  # creates n non-negative integers

# Cost Matrix cij
model.c = pyo.Param(model.N, model.M, initialize=lambda model, i, j: cost_matrix[i - 1][j - 1])


# Objective Function
def obj_func(model):
    return sum(model.x[i, j] * model.c[i, j] for i in model.N for j in model.M)


model.objective = pyo.Objective(rule=obj_func, sense=pyo.minimize)


# Constraints
def rule_const1(model, M):
    return sum(model.x[i, M] for i in model.N if i!= M) == 1


model.const1 = pyo.Constraint(model.M, rule=rule_const1)


def rule_const2(model, N):
    return sum(model.x[N, j] for j in model.M if j!= N) == 1


model.const2 = pyo.Constraint(model.N, rule=rule_const2)


def rule_const3(model, i, j):
    if i!= j:
        return model.u[i] - model.u[j] + model.x[i, j] * n <= n - 1
    else:
        return model.u[i] - model.u[i] == 0


model.rest3 = pyo.Constraint(model.U, model.N, rule=rule_const3)


# prints the entire model
model.pprint()

#Solves
solver = SolverFactory('glpk')
result = solver.solve(model)

# Print the result
print(result)

# Print values of the decision variables for which xij = 1
l = list(model.x.keys())
for i in l:
    if model.x[i]() != 0:
        print(i, '--', model.x[i]())
