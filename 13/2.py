with open('input.txt') as f:
	dots = []
	folds = []
	max_x = 0
	max_y = 0
	for line in f.readlines():
		if line.find(',') >= 0:
			tmp = line.strip().split(',')
			dots.append((int(tmp[0]), int(tmp[1])))
			max_x = max(max_x, int(tmp[0]))
			max_y = max(max_y, int(tmp[1]))
		if line.find('fold along') >= 0:
			folds.append(line.strip().split(' ')[2])

maps = []
for i in range(max_y + 1):
	maps.append(['.'] * (max_x + 1))

for dot in dots:
	maps[dot[1]][dot[0]] = '#'

def merge_dots(map1, map2):
	new_map = []
	for line1, line2 in zip(map1, map2):
		new_line = []
		for dot1, dot2 in zip(line1, line2):
			new_line.append('.' if dot1 == '.' and dot2 == '.' else '#')
		new_map.append(new_line)
	return new_map

for fold in folds:
	tmp = fold.split('=')
	fold_idx = int(tmp[1])
	if tmp[0] == 'x':
		map1 = list(map(lambda line: line[:fold_idx], maps))
		map2 = list(map(lambda line: line[fold_idx+1:][::-1], maps))
		maps = merge_dots(map1, map2)

	elif tmp[0] == 'y':
		map1, map2 = maps[:fold_idx], maps[fold_idx+1:]
		maps = merge_dots(map1, map2[::-1])

for line in maps:
	print(''.join(line))
