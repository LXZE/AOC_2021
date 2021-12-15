from collections import defaultdict as ddict
import heapq
import numpy as np

with open('input.txt') as f:
	maps = list(map(lambda line: list(map(int, line.strip())), f.readlines()))

update = lambda x: x+1 if x < 9 else 1
res = [np.array(maps)]
tmp = res[0]
for i in range(4):
	new_tmp = tmp.copy()
	tmp = np.vectorize(update)(new_tmp)
	res.append(tmp)
maps = np.concatenate(res, axis=1)
res = [maps.copy()]
tmp = res[0]
for i in range(4):
	new_tmp = tmp.copy()
	tmp = np.vectorize(update)(new_tmp)
	res.append(tmp)
maps = np.concatenate(res, axis=0)

def solve():
	h, w = len(maps), len(maps[0])
	queue = [(0, (0,0))]
	fp = ddict(lambda: float('inf'), { (0,0): 0 })
	visited = set()
	while queue:
		dist, pos = heapq.heappop(queue)
		if pos == (h-1, w-1): return dist
		if pos in visited: continue
		visited.add(pos)
		row, col = pos

		candidates = list(filter(
			lambda p: 0 <= p[0] < h and 0 <= p[1] < w,
			[(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
		))

		for c in candidates:
			new_dist = dist + maps[c[0]][c[1]]
			if new_dist < fp[c]:
				fp[c] = new_dist
				heapq.heappush(queue, (new_dist, c))

res = solve()
print(res)
