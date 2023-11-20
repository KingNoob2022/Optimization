import numpy as np

m, n = tuple(list(map(int,input().split())))
mat_A = []
for i in range(m):
	my_list = list(map(int,input().split()))
	mat_A.append(my_list)
vector_b = list(map(int,input().split()))
start_vector = list(map(int,input().split()))

mat_A = np.array(mat_A)
vector_b = np.array(vector_b)
start_vector = np.array(start_vector)
result_vector = start_vector
min_f = 1000000

num_epochs = 100000
alpha = 2
for i in range(num_epochs):
	result = np.matmul(mat_A, start_vector) + vector_b
	max_index = np.argmax(result)
	if min_f > np.max(result):
		min_f = np.max(result)
		result_vector = start_vector
	start_vector = np.subtract(start_vector, alpha * mat_A[max_index])

print(result_vector)
