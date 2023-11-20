import random


def argmin(ls):
    min_value = min(ls)
    return ls.index(min_value)


# Read the input data
num_cities = int(input())
route_matrix = []
read_data = open('data_large_TSP')
for line in read_data:
    data = list(map(int, line.split()))
    route_matrix.append(data)

first_city = random.randint(1, num_cities)


def find_min_tsp(first_city, num_cities, route_matrix):
    result = [first_city]
    for i in range(1, num_cities):
        list_x = [k for k in range(num_cities) if k + 1 not in result]
        j = argmin([route_matrix[result[-1] - 1][k] for k in list_x])
        result.append(list_x[j] + 1)
    return result


print(num_cities)
print(*find_min_tsp(first_city, num_cities, route_matrix))
