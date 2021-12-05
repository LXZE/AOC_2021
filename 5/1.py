from itertools import chain
from collections import Iterable

f = open('input.txt', 'r')

lines_list = list(map(lambda line: line.strip().split(' -> '), f.readlines()))
f.close()

def flatten(x):
    return chain.from_iterable([i] if not isinstance(i, Iterable) else i for i in x)

for idx, line in enumerate(lines_list):
	lines_list[idx] = list(map(lambda item: list(map(int, item.split(','))), line))

no_diag = []
max_dim = 0
for line in lines_list:
	max_dim = max(max(flatten(line)), max_dim)
	if line[0][0] == line[1][0] or line[0][1] == line[1][1]:
		no_diag.append(line)

# print(lines_list)
# print(no_diag)
# print(max_dim)

diagram = []
for i in range(max_dim+1):
	diagram.append([0] * (max_dim + 1))

for coord in no_diag:
	if coord[0][0] == coord[1][0]:
		min_idx, max_idx = min(coord[0][1], coord[1][1]), max(coord[0][1], coord[1][1])
		axis = 'col'
		fixed = coord[0][0]
	else:
		min_idx, max_idx = min(coord[0][0], coord[1][0]), max(coord[0][0], coord[1][0])
		axis = 'row'
		fixed = coord[0][1]
	
	# print(axis, coord, min_idx, max_idx, fixed)

	for idx in range(min_idx, max_idx+1):
		if axis == 'col':
			diagram[fixed][idx] += 1
		else:
			diagram[idx][fixed] += 1
res = 0
for line in diagram:
	res += sum(item > 1 for item in line)
print(res)
