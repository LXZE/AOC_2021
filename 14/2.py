from collections import defaultdict as ddict

with open('input.txt') as f:
	template = list(f.readline().strip())
	f.readline()
	pair = dict(map(lambda line: line.strip().split(' -> '), f.readlines()))

def create_new_count():
	return {k:0 for k in pair}
count = create_new_count()

for idx in range(len(template) - 1):
	count[''.join(template[idx:idx+2])] += 1

del_count = {chr(k):0 for k in range(65, 91)}
for c in template[1:-1]:
	del_count[c] += 1

limit = 40
for _ in range(limit):
	new_count = create_new_count()
	for k,v in count.items():
		if v > 0:
			pair_key = pair[k]
			new_count[''.join([k[0], pair[k]])] += v
			new_count[''.join([pair[k], k[1]])] += v
			del_count[pair_key] += v
	count = new_count

def count_char(counter):
	count = ddict(int)
	for k,v in counter.items():
		count[k[0]] += v
		count[k[1]] += v
	for k,v in del_count.items():
		if v > 0: count[k] -= v
	return sorted(count.items(), key=lambda k: -k[1])
res = count_char(count)
print(res[0][1] - res[-1][1])
