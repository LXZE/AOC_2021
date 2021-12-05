from itertools import chain
from collections import Iterable
import numpy as np

f = open('input.txt', 'r')

lines_list = list(map(lambda line: line.strip().split(' -> '), f.readlines()))
f.close()

def flatten(x):
    return chain.from_iterable([i] if not isinstance(i, Iterable) else i for i in x)

for idx, line in enumerate(lines_list):
	lines_list[idx] = sorted(list(map(lambda item: list(map(int, item.split(','))), line)))

max_dim = 0
for line in lines_list:
	max_dim = max(max(flatten(line)), max_dim)
# print(lines_list)
# print(max_dim)

diagram = []
for i in range(max_dim+1):
	diagram.append([0] * (max_dim + 1))

def get_line_type(coord):
	if coord[0][0] == coord[1][0]: return 'col'
	if coord[0][1] == coord[1][1]: return 'row'
	
	dx = coord[1][0] - coord[0][0]
	dy = coord[1][1] - coord[0][1]
	if dy / dx > 0: return 'dec' # because y incrased when go downward (kinda counterintuitive tho)
	return 'inc'

def print_diagram(dg):
	dg = np.array(dg).T
	for line in dg:
		tmp = list(map(lambda x: '.' if x == 0 else x, line))
		print(''.join(map(str, tmp)))

for coord in lines_list:
	axis = get_line_type(coord)

	# print(axis, coord)

	if axis == 'col':
		min_idx, max_idx = min(coord[0][1], coord[1][1]), max(coord[0][1], coord[1][1])
		fixed = coord[0][0]
	elif axis == 'row':
		min_idx, max_idx = min(coord[0][0], coord[1][0]), max(coord[0][0], coord[1][0])
		fixed = coord[0][1]

	elif axis == 'dec':
		size = coord[1][0] - coord[0][0]
		start = coord[0]
	else:
		size = coord[1][0] - coord[0][0]
		start = coord[0]

	if axis in ['col', 'row']:
		for idx in range(min_idx, max_idx+1):
			if axis == 'col':
				diagram[fixed][idx] += 1
			else:
				diagram[idx][fixed] += 1
	else:
		for offset in range(size + 1):
			if axis == 'dec':
				diagram[start[0] + offset][start[1] + offset] += 1
			else:
				diagram[start[0] + offset][start[1] - offset] += 1
	# print_diagram(diagram)
	# print('-'*20)

res = 0
diagram = np.array(diagram).T
for line in diagram:
	tmp = list(map(lambda x: '.' if x == 0 else x, line))
	# print(''.join(map(str, tmp)))
	res += sum(item > 1 for item in line)
print(res)
