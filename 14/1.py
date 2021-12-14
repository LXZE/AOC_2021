from collections import Counter

with open('input.txt') as f:
	template = list(f.readline().strip())
	f.readline()
	pair = dict(map(lambda line: line.strip().split(' -> '), f.readlines()))

step = 10
for _ in range(step):
	new_template = []
	for idx in range(len(template) - 1):
		chunk = ''.join(template[idx:idx+2])
		new_template.extend([template[idx], pair[chunk]])
	new_template.append(template[-1])
	template = new_template

counter = Counter(template)
res = sorted(counter.items(), key=lambda k: -k[1])
print(res[0][1] - res[-1][1])
