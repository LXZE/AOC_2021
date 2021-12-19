from itertools import combinations
from collections import defaultdict as ddict, Counter
from pprint import pprint

with open('input.txt') as f:
	scanners = []
	tmp = []
	for line in f.readlines():
		if line == '\n':
			scanners.append(tmp)
			tmp = []
		elif line[0:3] != '---':
			tmp.append(tuple(map(int, line.strip().split(','))))
scanners.append(tmp)

def calc_dist(a, b):
	return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def distance(beacons: list):
	distance_pair = []
	for pair in combinations(beacons, 2):
		dist = calc_dist(pair[0], pair[1])
		distance_pair.append((dist, pair[0], pair[1]))
	return distance_pair

def check_similarity(pair1: list, pair2: list):
	lookup = ddict(list)
	for item in pair1:
		lookup[item[0]].append(item[1:])
	found = []

	p2_list = []
	for p2 in pair2:
		if p2[0] in lookup:
			found.append(
				{'p1': lookup[p2[0]], 'p2': p2[1:], 'dist': p2[0]}
			)
			p2_list.extend(p2[1:])
	verifier = Counter(p2_list).most_common()

	res = []
	while len(verifier) > 0:
		candidate = verifier.pop(0)
		# find come pair that one point appears more than once
		tmp = list(filter(
			lambda item: candidate[0] in item['p2'] and len(item['p1']) == 1,
			found
		))
		# print('in check similarity')
		# print(tmp)
		if len(tmp) == 0: continue
		occur = ddict(int)
		for item in tmp:
			for p1 in item['p1']:
				occur[(candidate[0], p1[0])] += 1
				occur[(candidate[0], p1[1])] += 1
		# pprint(occur)
		max_confi = max(occur, key=occur.get)
		if occur[max_confi] <= 2: continue
		res.append((max_confi[1], max_confi[0]))
	# print(res)

	return (True, res) if len(res) >= 12 else (False, [])

# get relative position in 3d from two points
def diff(a, b):
	offset = [0,0,0]
	for idx in range(3):
		if idx == 1:
			offset[idx] = abs(abs(a[idx]) + abs(b[idx]))
		else:
			offset[idx] = abs(abs(a[idx]) - abs(b[idx]))
	return tuple(offset)

def find_orientation(candidates: list):
	guess = ddict(int)
	for c in candidates:
		src, tgt = c
		for i in range(3):
			for j in range(3):
				guess[(i,j,'+',src[i] + tgt[j])] += 1
				guess[(i,j,'-',src[i] - tgt[j])] += 1
	res = Counter(guess).most_common(3)
	tmp = res[0][1]
	assert all(g[1] == tmp for g in res[1:])
	# print('orientation')
	# pprint(res)
	return list(map(lambda x: x[0], res))

def calc(pos, orientation):
	res = [None] * 3
	for cmd in orientation: # cmd = tuple of (i, j, sign, offset)
		if cmd[2] == '+':
			res[cmd[0]] = pos[cmd[1]] - cmd[3]
			res[cmd[0]] = -res[cmd[0]]
		elif cmd[2] == '-':
			res[cmd[0]] = pos[cmd[1]] + cmd[3]
	return tuple(res)

beacons = scanners.pop(0)
breaker, limit = 0, len(scanners)
start_size = len(beacons)
while len(scanners) > 0:
	candidate_scanner = scanners.pop(0)
	beacons_pair = distance(beacons)
	new_beacons_pair = distance(candidate_scanner)
	result, checked_pair = check_similarity(beacons_pair, new_beacons_pair)

	if result:
		orientation = find_orientation(checked_pair)
		shifted_beacon = [calc(item, orientation) for item in candidate_scanner]
		beacons += shifted_beacon
		beacons = list(set(beacons))
	else:
		scanners.append(candidate_scanner)

	breaker += 1
	if breaker == limit:
		if len(beacons) == start_size:
			scanners.append(beacons)
			beacons = scanners.pop(0)

		breaker, limit = 0, len(scanners)
		start_size = len(beacons)

print(len(beacons))
