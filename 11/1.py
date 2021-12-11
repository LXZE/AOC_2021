with open('input.txt') as f:
	octopus = list(map(lambda line: list(map(int, line.strip())), f.readlines()))

def print_grid(grid):
	for line in grid:
		print(''.join(map(str, line)))

def update(grid):
	flash_count = 0

	# increase all
	flashed = set()
	to_updates = []
	for row in range(len(grid)):
		for col in range(len(grid[0])):
			grid[row][col] += 1
			if grid[row][col] >= 10:
				flashed.add((row, col))
				to_updates.extend(
					list(filter(
						lambda x: x[0] >= 0 and x[0] < len(grid) and x[1] >= 0 and x[1] < len(grid[0]),
						[(row + delta_row, col + delta_col) for delta_row in range(-1, 2) for delta_col in range(-1, 2)]
					))
				)

	# loop update
	while len(to_updates) > 0:
		row, col = to_updates.pop()
		if (row, col) in flashed: continue
		grid[row][col] += 1
		if grid[row][col] >= 10:
			flashed.add((row, col))
			to_updates.extend(
				list(filter(
					lambda x: x[0] >= 0 and x[0] < len(grid) and x[1] >= 0 and x[1] < len(grid[0]),
					[(row + delta_row, col + delta_col) for delta_row in range(-1, 2) for delta_col in range(-1, 2)]
				))
			)

	# clear
	for row in range(len(grid)):
		for col in range(len(grid[0])):
			if grid[row][col] >= 10:
				grid[row][col] = 0
				flash_count += 1
	return flash_count

res = 0
for step in range(100):
	res += update(octopus)
	# print(f'After step {step + 1}:')
	# print_grid(octopus)
print(res)
