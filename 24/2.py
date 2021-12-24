from functools import lru_cache
from typing import List

input_file = 'input'
with open(f'{input_file}.txt') as f:
	program = list(map(lambda line: line.strip().split(' '), f.readlines()))

block = []
tmp = []
for line in program:
	if line[0] == 'inp':
		block.append(tmp)
		tmp = []
	tmp.append(line)
block.append(tmp)
block = block[1:]

# explanation in 1.py
z1 = [int(code[4][2]) for code in block]
x1 = [int(code[5][2]) for code in block]
y1 = [int(code[15][2]) for code in block]
def run(i, w, z):
	x = (z % 26) + x1[i]
	z //= z1[i]
	if x != w:
		z *= 26
		z += w + y1[i]
	return z

limit_z = []
for z_idx in range(len(z1)):
	limit_z.append(26**len([z for z in z1[z_idx:] if z == 26]))

@lru_cache(maxsize=None)
def search(digit, current_z) -> List[str]:
	if digit == 14:
		return [''] if current_z == 0 else []
	if current_z > limit_z[digit]: return []
	res = []
	for w in list(range(1, 10)):
		next_z = run(digit, w, current_z)
		next_solution = search(digit + 1, next_z)
		for sol in next_solution:
			res.append(str(w) + sol)
	return res

solutions = search(0, 0)
solutions = list(map(int, solutions))
print(min(solutions))
