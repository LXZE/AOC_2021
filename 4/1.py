f = open('input.txt', 'r')

draw_list = list(map(int, f.readline().strip().split(',')))
f.readline()
lines = list(filter(lambda l: len(l) > 0, map(lambda l: l.strip().replace('  ', ' '), f.readlines())))
f.close()

boards = [list(map(lambda l: list(map(int, l.split(' '))), lines[i:i+5])) for i in range(0, len(lines), 5)]

for idx, board in enumerate(boards):
	boards[idx] = board + list(map(list, zip(*board)))

def check_win(boards):
	for idx, board in enumerate(boards):
		for line in board:
			if len(line) == 0:
				return (True, idx)

last = -1
for number in draw_list:
	for idx_board in range(len(boards)):
		for idx_line in range(len(boards[idx_board])):
			if number in boards[idx_board][idx_line]:
				boards[idx_board][idx_line].remove(number)
	last = number
	res = check_win(boards)
	if res and res[0]: break
found_board = [item for l in boards[res[1]][:5] for item in l]
print(sum(found_board) * last)
