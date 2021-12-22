input_file = 'test'
with open(f'{input_file}.txt') as f:
	cmd = []
	steps = []
	for line in f.readlines():
		c, l = line.strip().split(' ')
		cmd.append(c)
		l = l.split(',')
		l = list(map(lambda x: x.split('=')[1], l))
		l = list(map(lambda x: list(map(int, x.split('..'))), l))
		steps.append(l)

cubes = set()
for c, s in zip(cmd, steps):
	# print(f'now cube = {len(cubes)}')
	# print(s)
	skip = False
	for ax in s:
		if ax[0] > 50 or ax[1] < -50:
			# print(f'{s} skip because {ax}')
			skip = True
			break
	if skip: continue
	# fix loop to make sure it is in range -50..50
	for x in range(max(s[0][0], -50), min(s[0][1] + 1, 51)):
		for y in range(max(s[1][0], -50), min(s[1][1] + 1, 51)):
			for z in range(max(s[2][0], -50), min(s[2][1] + 1, 51)):
				if c == 'on':
					cubes.add((x, y, z))
				elif c == 'off':
					if (x, y, z) in cubes:
						cubes.remove((x, y, z))
print(len(cubes))
