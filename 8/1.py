with open('input.txt') as f:
	cmds = list(map(lambda line: line.strip().split(' | ')[1].split(' '), f.readlines()))
res = 0
for cmd in cmds:
	for digit in cmd:
		if len(digit) in [2,3,4,7]: res += 1
print(res)
