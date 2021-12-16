with open('input.txt') as f:
	data = list(map(lambda line: line.strip(), f.readlines()))
bin_mapper = {hex(k)[2:].capitalize():bin(k)[2:].zfill(4) for k in range(16)}

acc = 0
def parse(binary, given_idx):
	global acc
	idx = given_idx
	res = []
	for _ in range(2):
		res.append(binary[idx: idx+3])
		idx += 3
	acc += int(res[0], 2)
	if res[-1] == '100':
		while res[-1][0] != '0':
			res.append(binary[idx: idx+5])
			idx += 5
	else:
		res.append(binary[idx])
		idx += 1
		if res[-1] == '0':
			res.append(binary[idx: idx+15])
			idx += 15
			L = int(res[-1], 2)
			to_parse = binary[idx: idx+L]
			while len(to_parse) > 0:
				result, res_idx = parse(to_parse, 0)
				res.append(result)
				to_parse = to_parse[res_idx:]
				idx += res_idx

		else:
			res.append(binary[idx: idx+11])
			idx += 11
			L = int(res[-1], 2)
			to_parse = binary[idx:]
			for _ in range(L):
				result, res_idx = parse(to_parse, 0)
				res.append(result)
				to_parse = to_parse[res_idx:]
				idx += res_idx

	return (res, idx)

def solve(signal):
	global acc
	binary = ''
	for c in signal:
		binary += bin_mapper[c]
	acc = 0
	parse(binary, 0)
	print(acc)

for d in data:
	solve(d)
