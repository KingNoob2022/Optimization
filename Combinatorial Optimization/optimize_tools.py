from ortools.linear_solver import pywraplp

'''
# Create Solver
solver = pywraplp.Solver.CreateSolver("SCIP")
inf = solver.infinity()

# Create Variables
X1 = solver.NumVar(0, inf, 'X1')
X2 = solver.NumVar(0, inf, 'X2')


# Create constraints
cstr1 = solver.Constraint(-inf, 7)
cstr1.SetCoefficient(X1, 2)
cstr1.SetCoefficient(X2, 1)

cstr2 = solver.Constraint(-inf, 8)
cstr2.SetCoefficient(X1, 1)
cstr2.SetCoefficient(X2, 2)

cstr3 = solver.Constraint(-inf, 2)
cstr3.SetCoefficient(X1, 1)
cstr3.SetCoefficient(X2, -1)

# Create objective function
obj = solver.Objective()
obj.SetCoefficient(X1, 3)
obj.SetCoefficient(X2, 2)
obj.SetMaximization()

result_status = solver.Solve()

if result_status == pywraplp.Solver.OPTIMAL:
    print('optimal objective value =', solver.Objective().Value())
    print('X1 =', X1.solution_value(), ' X2 =', X2.solution_value())
else:
    print('The given problem does not have any optimal solution')
'''

num_var, num_inequality = tuple(list(map(int, input().split())))
co_obj = list(map(float, input().split()))
mat_A = []
for i in range(num_inequality):
    temp = list(map(float, input().split()))
    mat_A.append(temp)
vector_b = list(map(float, input().split()))


def create_data_model():
    """Stores the data for the problem."""
    data = {}
    data["constraint_coeffs"] = mat_A
    data["bounds"] = vector_b
    data["obj_coeffs"] = co_obj
    data["num_vars"] = num_var
    data["num_constraints"] = num_inequality
    return data


def main():
    data = create_data_model()
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return

    infinity = solver.infinity()
    x = {}
    for j in range(data["num_vars"]):
        x[j] = solver.IntVar(-infinity, infinity, "x[%i]" % j)
    # print("Number of variables =", solver.NumVariables())

    for i in range(data["num_constraints"]):
        constraint = solver.RowConstraint(-infinity, data["bounds"][i], "")
        for j in range(data["num_vars"]):
            constraint.SetCoefficient(x[j], data["constraint_coeffs"][i][j])
    # print("Number of constraints =", solver.NumConstraints())
    # In Python, you can also set the constraints as follows.
    # for i in range(data['num_constraints']):
    #  constraint_expr = \
    # [data['constraint_coeffs'][i][j] * x[j] for j in range(data['num_vars'])]
    #  solver.Add(sum(constraint_expr) <= data['bounds'][i])

    objective = solver.Objective()
    for j in range(data["num_vars"]):
        objective.SetCoefficient(x[j], data["obj_coeffs"][j])
    objective.SetMaximization()
    # In Python, you can also set the objective as follows.
    # obj_expr = [data['obj_coeffs'][j] * x[j] for j in range(data['num_vars'])]
    # solver.Maximize(solver.Sum(obj_expr))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Objective value =", solver.Objective().Value())
        res_list = []
        for j in range(data["num_vars"]):
            res_list.append(x[j].solution_value())
        print(*res_list)
        # print("Problem solved in %f milliseconds" % solver.wall_time())
        # print("Problem solved in %d iterations" % solver.iterations())
        # print("Problem solved in %d branch-and-bound nodes" % solver.nodes())
    else:
        print("The problem does not have an optimal solution.")


if __name__ == "__main__":
    main()


