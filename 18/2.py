import re, math, json
from itertools import permutations

with open('input.txt') as f:
	data = list(map(lambda l: l.strip(), f.readlines()))

def plus(a, b):
	return f'[{a},{b}]'

def explode(eq: str):
	new_eq = list(eq)
	stack = []
	for idx, char in enumerate(eq):
		if char == '[':
			stack.append(idx)
		elif char == ']':
			latest = stack.pop()
			if len(stack) >= 4:
				left, right = map(int, eq[latest+1: idx].split(','))
				to_update_left = [m for m in re.finditer(r'\d+', eq[:latest])]
				to_update_right = [m for m in re.finditer(r'\d+', eq[idx+1:])]

				offsetleft = 0
				if len(to_update_left) > 0:
					idxleft = to_update_left[-1].span()
					numleft = int(eq[idxleft[0]: idxleft[1]])
					newnumleft = numleft + left

					l = new_eq[:idxleft[0]]
					m = list(str(newnumleft))
					r = new_eq[idxleft[1]:]
					new_eq = l + m + r

					if len(str(numleft)) < len(str(newnumleft)):
						offsetleft = 1 # add offset 1 digit
				
				if len(to_update_right) > 0:
					shiftedidxright = to_update_right[0].span()
					idxright = (
						shiftedidxright[0] + idx + 1,
						shiftedidxright[1] + idx + 1
					)
					numright = int(eq[idxright[0]: idxright[1]])
					newnumright = numright + right

					l = new_eq[:idxright[0] + offsetleft]
					m = list(str(newnumright))
					r = new_eq[idxright[1] + offsetleft:]
					new_eq = l + m + r
				new_eq = new_eq[:latest+offsetleft] + ['0'] + new_eq[idx+1+offsetleft:]
				break
	return ''.join(new_eq)

def split(eq: str):
	to_update = [m for m in re.finditer(r'\d\d', eq)]
	if len(to_update) > 0:
		idx = to_update[0].span()
		num = int(eq[idx[0]: idx[1]])
		l, r = math.floor(num/2), math.ceil(num/2)
		return eq[:idx[0]] + f'[{l},{r}]' + eq[idx[1]:]
	return eq

def calc(eq):
	if type(eq) != list: return eq
	return (calc(eq[0]) * 3) + (calc(eq[1]) * 2)

max_magnitude = float('-inf')
combi = list(permutations(data, 2))
for a, b in combi:
	current_eq = plus(a, b)
	mode = 'exp'	
	while mode != 'fin':
		if mode == 'exp':
			new_eq = explode(current_eq)
			if new_eq == current_eq:
				mode = 'split'
			current_eq = new_eq
		elif mode == 'split':
			new_eq = split(current_eq)
			if new_eq == current_eq:
				mode = 'fin'
			else: mode = 'exp'
			current_eq = new_eq
	max_magnitude = max(max_magnitude, calc(json.loads(current_eq)))
print(max_magnitude)
