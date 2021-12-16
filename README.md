# LXZE's 2021 Advent of Code solutions

This repository is dedicated to archiving my solutions for questions in [Advent of Code 2021](https://adventofcode.com/2021), separating each question to each folder by its released date.  

Read it at your own risk.  

## Note 
- Day 15
	- First approach: [Dijkstra + heapq](https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/)
	- Second approach:  [networkx](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html)
	```python
	G = nx.Graph()
	h, w = len(maps), len(maps[0])
	for r in range(h):
		for c in range(w):
			for e in list(filter(
				lambda p: 0 <= p[0] < h and 0 <= p[1] < w,
				[(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
			)): G.add_edge((r, c), e)
	# check weight here instead of assign while adding edge
	weight_func = lambda u,v,d: maps[v[0]][v[1]]
	res = nx.dijkstra_path(G, (0, 0), (w-1, h-1), weight=weight_func)
	print(reduce(lambda acc, p: acc+maps[p[0]][p[1]], res[1:], 0))
	```