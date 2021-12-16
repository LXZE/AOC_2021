from functools import reduce

with open('input.txt') as f:
	data = list(map(lambda line: line.strip(), f.readlines()))
bin_mapper = {hex(k)[2:].capitalize():bin(k)[2:].zfill(4) for k in range(16)}

def parse(binary, given_idx):
	idx = given_idx
	res = []
	for _ in range(2):
		res.append(binary[idx: idx+3])
		idx += 3
	if res[-1] == '100':
		tmp = ['1']
		while tmp[-1][0] != '0':
			tmp.append(binary[idx: idx+5])
			idx += 5
		res.append(int(''.join(list(map(lambda x: x[1:], tmp))), 2))
		
	else:
		ops = int(res[-1], 2)
		len_id = binary[idx]
		idx += 1
		tmp = []
		if len_id == '0':
			tmp.append(binary[idx: idx+15])
			idx += 15
			L = int(tmp[-1], 2)
			to_parse = binary[idx: idx+L]
			while len(to_parse) > 0:
				result, res_idx = parse(to_parse, 0)
				tmp.append(result)
				to_parse = to_parse[res_idx:]
				idx += res_idx

		else:
			tmp.append(binary[idx: idx+11])
			idx += 11
			L = int(tmp[-1], 2)
			to_parse = binary[idx:]
			for _ in range(L):
				result, res_idx = parse(to_parse, 0)
				tmp.append(result)
				to_parse = to_parse[res_idx:]
				idx += res_idx

		if ops == 0:
			res.append(reduce(lambda acc, item: acc + item[2], tmp[1:], 0))
		elif ops == 1:
			res.append(reduce(lambda acc, item: acc * item[2], tmp[1:], 1))
		elif ops == 2:
			res.append(min(p[2] for p in tmp[1:]))
		elif ops == 3:
			res.append(max(p[2] for p in tmp[1:]))
		elif ops == 5:
			res.append(1 if tmp[1][2] > tmp[2][2] else 0)
		elif ops == 6:
			res.append(1 if tmp[1][2] < tmp[2][2] else 0)
		elif ops == 7:
			res.append(int(tmp[1][2] == tmp[2][2]))
		
	return (res, idx)

def solve(signal):
	binary = ''
	for c in signal:
		binary += bin_mapper[c]
	result, _ = parse(binary, 0)
	print(result[2])

for d in data:
	solve(d)
