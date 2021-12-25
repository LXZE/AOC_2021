import re
from os import system

input_file = 'input'
with open(f'{input_file}.txt') as f:
	plot = list(map(lambda line: line.strip(), f.readlines()))

cucumber = { '>': set(), 'v': set() }
h, w = len(plot), len(plot[0])

for row, line in enumerate(plot):
	for item in re.finditer(r'>', line):
		cucumber['>'].add((row, item.start()))
	for item in re.finditer(r'v', line):
		cucumber['v'].add((row, item.start()))

def plot_map(cucumber):
	for row in range(h):
		tmp = ''
		for col in range(w):
			if (row, col) in cucumber['>']:
				tmp += '>'
			elif (row, col) in cucumber['v']:
				tmp += 'v'
			else:
				tmp += '.'
		print(tmp)

res = 1
# plot_map(cucumber)
while True:
	change = False
	new_cucumber_r = set()
	for pos in cucumber['>']:
		new_pos = (pos[0], (pos[1] + 1) % w)
		if new_pos in cucumber['v'] or new_pos in cucumber['>']:
			new_cucumber_r.add(pos)
		else:
			new_cucumber_r.add(new_pos)
			change = True
	cucumber['>'] = new_cucumber_r
	new_cucumber_d = set()
	for pos in cucumber['v']:
		new_pos = ((pos[0] + 1) % h, pos[1])
		if new_pos in cucumber['v'] or new_pos in new_cucumber_r:
			new_cucumber_d.add(pos)		
		else:
			new_cucumber_d.add(new_pos)
			change = True
	cucumber['v'] = new_cucumber_d
	if not change: break
	res += 1
	# system('clear')
	# print('-' * 50)
	# plot_map(cucumber)
print(res)
