cmd = []
with open('input.txt', 'r') as f:
	cmd = list(map(lambda l: l.strip().split(' '), f.readlines()))

horizon_pos = 0
deep = 0
aim = 0
for c in cmd:
	if c[0] == 'forward':
		val = int(c[1])
		horizon_pos += val
		deep += aim * val
	elif c[0] == 'down':
		aim += int(c[1])
	elif c[0] == 'up':
		aim -= int(c[1])
print(horizon_pos*deep)