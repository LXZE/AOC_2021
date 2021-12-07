from functools import reduce

with open('input.txt') as f:
	pos_list = sorted(list(map(int, f.readline().strip().split(','))))

check = lambda target: reduce(lambda acc, item: abs(target - item) + acc, pos_list, 0)

start = sum(pos_list)//len(pos_list)
res = check(start)
for offset in range(1, max(abs(start - pos_list[0]), abs(start - pos_list[-1])) + 1):
	print(offset)
	if start - offset < 0: continue
	else: res = min(res, check(start - offset))
	if start + offset > pos_list[-1]: continue
	else: res = min(res, check(start + offset))
print(res)
