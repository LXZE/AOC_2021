with open('input.txt') as f:
	maps = list(map(lambda line: list(map(int, line.strip())), f.readlines()))

def is_low(row, col):
	return  maps[row][col] < (10 if row+1 >= len(maps) else maps[row+1][col]) \
		and maps[row][col] < (10 if row-1 < 0 else maps[row-1][col]) \
		and maps[row][col] < (10 if col-1 < 0 else maps[row][col-1]) \
		and maps[row][col] < (10 if col+1 >= len(maps[0]) else maps[row][col+1])

res = 0
for i, line in enumerate(maps):
	for j, val in enumerate(line):
		if is_low(i, j):
			res += val + 1
print(res)
