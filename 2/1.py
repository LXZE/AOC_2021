cmd = []
with open('input.txt', 'r') as f:
	cmd = list(map(lambda l: l.strip().split(' '), f.readlines()))

dist = 0
deep = 0
for c in cmd:
	if c[0] == 'forward':
		dist += int(c[1])
	elif c[0] == 'down':
		deep += int(c[1])
	elif c[0] == 'up':
		deep -= int(c[1])
print(dist*deep)