with open('input.txt') as f:
	paths = list(map(lambda line: line.strip().split('-'), f.readlines()))

def get_target(current, link):
	return link[1] if current == link[0] else link[0]

res = []
def loop(current, prev, memory):
	if current == 'end':
		res.append(prev + [current])
		return

	to_explore = []
	for path in paths:
		if current in path:
			candidate = get_target(current, path)
			if candidate not in memory:
				to_explore.append(candidate)

	# print(f'current: {current}, to_explore: {to_explore}')
	for t in to_explore:
		if t in memory: continue
		new_mem = memory.copy()
		if t.islower(): new_mem.add(t)
		loop(t, prev + [current], new_mem)

loop('start', [], set(['start']))
print(len(res))
