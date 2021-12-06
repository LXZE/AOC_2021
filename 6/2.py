from collections import Counter

with open('input.txt') as f:
	states = list(map(int, f.readline().strip().split(',')))

counter = dict(Counter(states))
def loop(day,p0,p1,p2,p3,p4,p5,p6,p7,p8):
	if day == 0: return sum([p0,p1,p2,p3,p4,p5,p6,p7,p8])
	return loop(day-1, p1, p2, p3, p4, p5, p6, p7 + p0, p8, p0)

res = loop(256, 0, counter[1], counter[2], counter[3], counter[4], counter[5], 0,0,0)
print(res)
