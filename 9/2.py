from functools import reduce

with open('input.txt') as f:
	maps = list(map(lambda line: list(map(int, line.strip())), f.readlines()))

def is_low(row, col):
	return  maps[row][col] < (10 if row+1 >= len(maps) else maps[row+1][col]) \
		and maps[row][col] < (10 if row-1 < 0 else maps[row-1][col]) \
		and maps[row][col] < (10 if col-1 < 0 else maps[row][col-1]) \
		and maps[row][col] < (10 if col+1 >= len(maps[0]) else maps[row][col+1])

candidates = []
for i, line in enumerate(maps):
	for j, val in enumerate(line):
		if is_low(i, j):
			candidates.append((i, j))

def expand(row, col):
	branch = [(row, col)]
	visited = set()
	while len(branch) > 0:
		point = branch.pop()
		if point in visited:
			continue
		elif maps[point[0]][point[1]] == 9:
			continue
		visited.add(point)
		branch.extend(
			list(filter(
				lambda loc: loc[0] >= 0 and loc[0] < len(maps) and loc[1] >= 0 and loc[1] < len(maps[0]),
				[(point[0]+1, point[1]), (point[0]-1, point[1]), (point[0], point[1]+1), (point[0], point[1]-1)]
			))
		)
	return len(visited)

res = []
for point in candidates:
	res.append(expand(*point))
print(reduce(lambda acc, item: acc * item, sorted(res)[-3:], 1))
