import numpy as np

num_var, num_inequality = tuple(list(map(int, input().split())))
coef_z = list(map(float, input().split()))
mat_A = []
for i in range(num_inequality):
	coef = list(map(float, input().split()))
	mat_A.append(coef)
coef_z = np.array(coef_z)
coef_z *= -1
mat_A.append(coef_z)
mat_A = np.array(mat_A)
identity_mat = np.identity(num_inequality + 1)
mat_A = np.concatenate((mat_A, identity_mat), axis = 1)

rhs = list(map(float, input().split()))
rhs.append(0)
rhs = np.array(rhs)

is_unbounded = False


def check_positive(vect):
	for i in vect:
		if i < 0:
			return False
	return True


while not check_positive(mat_A[num_inequality]):
	min_index = np.argmin(mat_A[num_inequality])
	local_min = 99999999
	row_index = 0
	count = 0
	for i in range(num_inequality):
		if mat_A[i, min_index] <= 0:
			count += 1
			continue
		else:
			evaluation = rhs[i] / mat_A[i, min_index]
			if local_min > evaluation:
				local_min = evaluation
				row_index = i
	if count == num_inequality:
		is_unbounded = True
		break
	temp1 = mat_A[row_index, min_index]
	mat_A[row_index] = mat_A[row_index] / mat_A[row_index, min_index]
	rhs[row_index] /= temp1
	for i in range(num_inequality + 1):
		if i == row_index:
			continue
		else:
			temp = mat_A[i, min_index]
			mat_A[i] -= mat_A[i, min_index] * mat_A[row_index]
			rhs[i] -= temp * rhs[row_index]

if not is_unbounded:
	print(num_var)
	list_number = []
	for i in range(len(mat_A[num_inequality])):
		if mat_A[num_inequality, i] > 0:
			list_number.append(i)
	sub_mat = []
	for i in range(num_inequality):
		temp = []
		for j in range(len(mat_A[i])):
			if j not in list_number:
				temp.append(mat_A[i, j])
		sub_mat.append(temp)
	sub_mat = np.array(sub_mat)
	sol = np.linalg.solve(sub_mat, rhs[0:-1])
	count = 0
	optimize_sol = []
	for i in range(num_var):
		if i in list_number:
			optimize_sol.append(0)
		else:
			optimize_sol.append(sol[count])
			count += 1
	print(*optimize_sol)
else:
	print("UNBOUNDED")
