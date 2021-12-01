data = []
with open('input.txt', 'r') as f:
	data = list(map(lambda l: int(l.strip()), f.readlines()))
res = 0
for i in range(len(data)):
	if i < 3: continue
	tmp = data[i-1] + data[i-2]
	if tmp + data[i] > tmp + data[i-3]:
		res += 1
print(res)