with open('input.txt') as f:
	paths = list(map(lambda line: line.strip().split('-'), f.readlines()))

def get_target(current, link):
	return link[1] if current == link[0] else link[0]

res = set()

def loop(current, prev, memory):
	# print(f'current: {current}, prev: {prev}, memory: {memory}')
	if current == 'end':
		res.add(','.join(prev + [current]))
		return

	to_explore = []
	for path in paths:
		if current in path:
			candidate = get_target(current, path)
			to_explore.append(candidate)

	# print(f'to_explore: {to_explore}')
	for t in to_explore:
		if t == 'start': continue
		new_mem = memory.copy()
		# if t exists in memory, check if twice is selected
		if t in new_mem:
			if new_mem['twice'] == t and new_mem[t] == 1:
				new_mem[t] += 1
				loop(t, prev + [current], new_mem)
		else:
			if t.islower():
				new_mem[t] = 1
				if new_mem['twice'] == '':
					loop(t, prev + [current], new_mem)
					new_mem2 = new_mem.copy()
					new_mem2['twice'] = t
					loop(t, prev + [current], new_mem2)
				else:
					loop(t, prev + [current], new_mem)
			else:
				loop(t, prev + [current], new_mem)

loop('start', [], { 'twice': '', 'start': 1 })
print(len(res))
