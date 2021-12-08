from functools import reduce

with open('input.txt') as f:
	signal_cmds = list(map(lambda line: line.strip().split(' | '), f.readlines()))

mapper = [
	[1, 1, 1, 0, 1, 1, 1],
	[0, 0, 1, 0, 0, 1, 0],
	[1, 0, 1, 1, 1, 0, 1],
	[1, 0, 1, 1, 0, 1, 1],
	[0, 1, 1, 1, 0, 1, 0],
	[1, 1, 0, 1, 0, 1, 1],
	[1, 1, 0, 1, 1, 1, 1],
	[1, 0, 1, 0, 0, 1, 0],
	[1, 1, 1, 1, 1, 1, 1],
	[1, 1, 1, 1, 0, 1, 1],
]

def solve(key, cmd):
	block = [0]*7
	for char in cmd:
		block[key.index(char)] = 1
	return mapper.index(block)

res = 0
for entry in signal_cmds:
	signal = sorted(entry[0].split(' '), key=len)
	key = [-1]*7
	# find a
	key[0] = (set(signal[1]) - set(signal[0])).pop()

	# find c
	six_signal_members = signal[6:9]
	six = [(idx, item) for idx, item in enumerate(six_signal_members) if not set(signal[0]).issubset(set(item))]
	assert len(six) == 1
	six_signal_members.pop(six[0][0])
	six = six[0][1]
	key[2] = (set(signal[-1]) - set(six)).pop()
	# find f
	key[5] = (set(signal[0]) - set(key[2])).pop()

	# find d
	bd_set = set(signal[2]) - set(signal[0])
	zero = [(idx, item) for idx, item in enumerate(six_signal_members) if not bd_set.issubset(set(item))]
	assert len(zero) == 1
	six_signal_members.pop(zero[0][0])
	zero = zero[0][1]
	key[3] = (set(signal[-1]) - set(zero)).pop()
	# find b
	key[1] = (bd_set - set(key[3])).pop()

	# find e
	assert len(six_signal_members) == 1
	nine = six_signal_members[0]
	key[4] = (set(signal[-1]) - set(nine)).pop()
	# find g
	key[6] = (set(signal[-1]) - set(key[:-1])).pop()

	output = list(map(lambda cmd: solve(key, cmd), entry[1].split(' ')))
	result = reduce(lambda acc, item: acc + (item[1] * pow(10, item[0])), enumerate(output[::-1]), 0)
	
	res += result
print(res)
