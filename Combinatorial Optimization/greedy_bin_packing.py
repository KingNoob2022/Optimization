# Create Vehicle class and Order class
class Order:
    tag = 1

    def __init__(self, quantity, cost):
        self.quantity = quantity
        self.cost = cost
        self.index = Order.tag
        self.served_vehicle = None
        Order.tag += 1

    def __str__(self):
        return f"The order has quantity {self.quantity} and cost {self.cost}"


class Vehicle:
    tag = 1

    def __init__(self, lower_capacity, upper_capacity):
        self.lower_capacity = lower_capacity
        self.upper_capacity = upper_capacity
        self.current_capacity = 0
        self.served_order = 0
        self.order_cost = 0
        self.index = Vehicle.tag
        Vehicle.tag += 1

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
# Another way to read data
# num_of_orders, num_of_vehicles = tuple(map(int, input().split()))
# for i in range(num_of_orders):
#     quantity, cost = tuple(map(int, input().split()))
#     orders.append(Order(quantity, cost))
# for i in range(num_of_vehicles):
#     lower_bound, upper_bound = tuple(map(int, input().split()))
#     vehicles.append(Vehicle(lower_bound, upper_bound))


# Sort the vehicles in non-increasing order based on upper capacity
initial_vehicles = vehicles[:]
vehicles.sort(key=lambda x: x.upper_capacity, reverse=True)
# Sort the orders in non-increasing order based on quantity
initial_orders = orders[:]
orders.sort(key=lambda x: float(x.cost), reverse=True)

# Set up the necessary variables
order_distribution = dict()
available = [True] * num_of_vehicles
current_order_list = orders[:]
num_of_served_order = 0
total_cost = 0


# Implement Greedy Algorithm
def feasible(order, vehicle, vehicle_index):
    x = vehicle.current_capacity + order.quantity
    first_condition = x <= vehicle.upper_capacity
    if first_condition:
        temp = current_order_list[:]
        temp.remove(order)
        if len(temp) > 0:
            if x + min([z.quantity for z in temp]) > vehicle.upper_capacity:
                if x < vehicle.lower_capacity:
                    return False
                else:
                    available[vehicle_index] = False
                    return True
            else:
                return True
        else:
            if x < vehicle.lower_capacity:
                return False
            else:
                available[vehicle_index] = False
                return True
    return False


for i in range(num_of_orders):
    take_order = False
    for j in range(num_of_vehicles):
        if available[j]:
            if feasible(orders[i], vehicles[j], j):
                orders[i].served_vehicle = vehicles[j]
                vehicles[j].served_order += 1
                vehicles[j].order_cost += orders[i].cost
                current_order_list.remove(orders[i])
                if vehicles[j].index not in order_distribution.keys():
                    order_distribution[vehicles[j].index] = [orders[i].index]
                else:
                    order_distribution[vehicles[j].index].append(orders[i].index)
                vehicles[j].current_capacity += orders[i].quantity
                take_order = True
        if take_order:
            break


for key in order_distribution.keys():
    # print(f"Truck {key} takes orders: {order_distribution[key]}")
    v = initial_vehicles[key - 1]
    if v.lower_capacity <= v.current_capacity <= v.upper_capacity:
        num_of_served_order += v.served_order
        total_cost += v.order_cost
        print(f"Truck {key}: current capacity {v.current_capacity}, lower capacity {v.lower_capacity}, upper capacity {v.upper_capacity}")
print(num_of_served_order)
print(total_cost)
# print()
# Alternative display
# print(num_of_served_order)
# for item in initial_orders:
#     if item.served_vehicle is not None:
#         v = item.served_vehicle
#         if v.lower_capacity <= v.current_capacity <= v.upper_capacity:
#             print(f"{item.index} {item.served_vehicle.index}")
