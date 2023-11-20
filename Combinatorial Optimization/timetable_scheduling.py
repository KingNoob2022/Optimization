import time

# Start timer
start_time = time.time()
# Define the Class
class Class:
    def __init__(self, periods, teacher, students):
        self.num_of_periods = periods
        self.teacher = teacher
        self.num_of_students = students

    def __str__(self):
        return f"Number of periods is: {self.num_of_periods}, teacher is: {self.teacher}, number of students is: {self.num_of_students}"

class Room:
    def __init__(self, seats):
        self.num_of_seats = seats

    def __str__(self):
        return f"Number of seats is: {self.num_of_seats}"


# Import the libraries
from ortools.sat.python import cp_model

# Get the data
classes = []
rooms = []
num_of_classes, num_of_rooms = 0, 0

read_data = open('input_data.txt')
count = 0
for line in read_data:
    if count == 0:
        num_of_classes, num_of_rooms = tuple(map(int, line.split()))
        count += 1
    elif count <= num_of_classes:
        a, b, c = tuple(map(int, line.split()))
        classes.append(Class(a, b, c))
        count += 1
    else:
        data = list(map(int, line.split()))
        if len(data) != num_of_rooms:
            print("Invalid number of rooms")
        else:
            for i in data:
                rooms.append(Room(i))

total_slots = range(60)
all_classes = range(num_of_classes)
all_rooms = range(num_of_rooms)
# Create the model
model = cp_model.CpModel()

# Create the variables:
periods = {}
for c in all_classes:
    for s in total_slots:
        for r in all_rooms:
            periods[(c, s, r)] = model.NewIntVar(0, 1, f"period_c{c}_s{s}_r{r}")


'''Add the constraints'''
for c in all_classes:
    for s in total_slots:
        for r in all_rooms:
            model.Add(periods[(c, s, r)] * (s + classes[c].num_of_periods) <= 59)

# Number of seats in the room >= number of students in that class
for c in all_classes:
    for s in total_slots:
        for r in all_rooms:
            model.Add(periods[(c, s, r)] * (classes[c].num_of_students - rooms[r].num_of_seats) <= 0)

# Total periods in 1 day <= 12 periods
for r in all_rooms:
    for j in range(1, 6):
        model.Add(sum(periods[(c, s, r)] * classes[c].num_of_periods for c in all_classes for s in range(12 * (j-1), 12 * j)) <= 12)

for c in all_classes:
    for s in total_slots:
        model.Add(sum(periods[(c, s, r)] for r in all_rooms) * (s % 12 + classes[c].num_of_periods) <= 12)

# A class doesn't study simultaneously at 2 room
for c in all_classes:
    for s in total_slots:
        model.Add(sum(periods[(c, s, r)] for r in all_rooms) <= 1)

# A class study only once a week
for c in all_classes:
    model.Add(sum(periods[(c, s, r)] for s in total_slots for r in all_rooms) <= 1)

# A classroom doesn't have 2 class simultaneously
for r in all_rooms:
    for c in all_classes:
        for s in range(61 - classes[c].num_of_periods):
            model.Add(sum(periods[(new_c, new_s, r)] for new_c in all_classes for new_s in range(s, s + classes[c].num_of_periods)) == 1).OnlyEnforceIf(periods[(c, s, r)])

# A teacher isn't assigned to a class at the same time
instructor_dict = {}
for i in range(len(classes)):
    if classes[i].teacher not in instructor_dict.keys():
        instructor_dict[classes[i].teacher] = [i]
    else:
        instructor_dict[classes[i].teacher].append(i)
for key in instructor_dict.keys():
    for c in instructor_dict[key]:
        for s in range(61 - classes[c].num_of_periods):
            for new_r in all_rooms:
                model.Add(sum(periods[(c1, s1, r)] for c1 in instructor_dict[key] for s1 in range(s, s + classes[c].num_of_periods) for r in all_rooms) == 1).OnlyEnforceIf(periods[(c, s, new_r)])


# Set up the objective function
model.Maximize(sum(periods[(c, s, r)] * (60 - s) for c in all_classes for s in total_slots for r in all_rooms))

# Invoke the solver
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Display the result
if status == cp_model.OPTIMAL:
    print("Solution:")
    for c in all_classes:
        for s in total_slots:
            for r in all_rooms:
                if solver.Value(periods[(c, s, r)]) == 1:
                    print("Class", c + 1, "Teacher", classes[c].teacher, "Number of periods", classes[c].num_of_periods, "Slot", s + 1, "Room", r + 1, "(requested).")
    print(
        f"Number of shift requests met = {solver.ObjectiveValue()}"
    )
else:
    print("No optimal solution found !")

# End timer
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time)