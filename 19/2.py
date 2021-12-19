from pprint import pprint
from itertools import combinations as combi, permutations as permut, chain
from collections import defaultdict as ddict, Counter

with open('input.txt') as f:
	idx = 0
	scanners = []
	tmp = []
	for line in f.readlines():
		if line == '\n':
			scanners.append(tmp)
			idx += 1
			tmp = []
		elif line[0:3] != '---':
			tmp.append(tuple(map(int, line.strip().split(','))))
scanners.append(tmp)
total_scanners = len(scanners)

confident_number = 12

def powerset(iterable):
	s = list(iterable)
	return chain.from_iterable(combi(s, r) for r in range(len(s)+1))

coord_remaps = [x for x in permut(range(3), 3)]
coord_negations = []
for p in powerset(range(3)):
	res = [1,1,1]
	for idx in p: res[idx] = -1
	coord_negations.append(tuple(res))

def apply(remap, negate, pos):
	res = []
	for item in pos:
		res.append([negate[i]*item[remap[i]] for i in range(3)])
	return res

def distance(a, b):
	return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def distance_each_pair(beacons: list):
	distance_pair = []
	for pair in combi(beacons, 2):
		distance_pair.append((distance(pair[0], pair[1]), pair[0], pair[1]))
	return distance_pair

distances_from_0 = [(0,0,0)]
def find_alignment(beacons, candidates):
	lookup = ddict(list)
	beacon_distance_pair = distance_each_pair(beacons)
	candidate_distance_pair = distance_each_pair(candidates[0])

	for item in beacon_distance_pair:
		lookup[item[0]].append(item[1:])
	found = []

	p2_list = []
	for p2 in candidate_distance_pair:
		if p2[0] in lookup:
			found.append(
				{'p1': lookup[p2[0]], 'p2': p2[1:], 'dist': p2[0]}
			)
			p2_list.extend(map(tuple, p2[1:]))
	verifier = Counter(p2_list).most_common()
	res = []
	while len(verifier) > 0:
		cdd = verifier.pop(0)
		tmp = list(filter(
			lambda item: list(cdd[0]) in item['p2'] and len(item['p1']) == 1,
			found
		))
		# print('in check similarity')
		# print(cdd, tmp)
		if len(tmp) == 0: continue
		occur = ddict(int)
		for item in tmp:
			for p1 in item['p1']:
				occur[(cdd[0], p1[0])] += 1
				occur[(cdd[0], p1[1])] += 1
		# pprint(occur)
		max_confi = max(occur, key=occur.get)
		if occur[max_confi] <= 2: continue
		res.append((max_confi[1], max_confi[0]))
	# check relative orientation for each translated candidate scanner with main scanner
	if len(res) >= confident_number:
		# print('check match')
		for translated in candidates:
			for beacon in beacons:
				for candidate in translated:
					shifted = [a-b for a,b in zip(candidate, beacon)]
					match = 0
					all_shifted = []
					for other_candidate in translated:
						shifted_to_beacon = tuple([a-b for a,b in zip(other_candidate, shifted)])
						if shifted_to_beacon in beacons:
							match += 1
						all_shifted.append(list(shifted_to_beacon))
					if match >= confident_number:
						distances_from_0.append(tuple(shifted))
						return (True, all_shifted)
	return (False, None)

candidates = {}
for idx, scanner in enumerate(scanners[1:]):
	candidates[idx+1] = [
		apply(remap, negate, scanner)
		for remap in coord_remaps for negate in coord_negations
	]

aligned_index = set([0])
aligned = {0: list(map(tuple, scanners[0]))}
all_aligned = set([tuple(x) for x in scanners[0]])
not_aligned = set()
while len(aligned_index) < len(scanners):
	for idx in range(total_scanners):
		if idx in aligned_index: continue
		for a_idx in aligned_index:
			# print(f'check {idx} to {a_idx} in {aligned_index}')
			if (idx, a_idx) in not_aligned: continue
			ok, remap = find_alignment(aligned[a_idx], candidates[idx])
			if ok:
				# print(f'merge {idx}')
				aligned_index.add(idx)
				aligned[idx] = list(map(tuple, remap))
				all_aligned |= set([tuple(x) for x in remap])
				break
			not_aligned.add((idx, a_idx))
# print(len(all_aligned))
# pprint(distances_from_0)

def calc(scanners_pos):
	max_dist = 0
	for a, b in combi(scanners_pos, 2):
		max_dist = max(max_dist, distance(a, b))
	return max_dist
print(calc(distances_from_0))
