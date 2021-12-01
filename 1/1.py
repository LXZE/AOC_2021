data = []
with open('input.txt', 'r') as f:
	data = list(map(lambda l: int(l.strip()), f.readlines()))
res = 0
for i in range(len(data)):
	if i == 0: continue
	if data[i] > data[i-1]:
		res += 1
print(res)