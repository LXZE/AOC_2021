import re
from collections import defaultdict as ddict
from itertools import permutations as permu, combinations as combi, product
from functools import lru_cache
from pprint import pprint
from typing import Tuple, List

input_file = 'input'
with open(f'{input_file}.txt') as f:
	program = list(map(lambda line: line.strip().split(' '), f.readlines()))

# 2nd attempt: find pattern in assembly
block = []
tmp = []
for line in program:
	if line[0] == 'inp':
		block.append(tmp)
		tmp = []
	tmp.append(line)
block.append(tmp)
block = block[1:]
# there are 14 blocks
# each start with
'''
inp w
mul x 0 # x = 0
add x z # x += z
mod x 26 # x %= 26
'''
# then div z which variate upon each step
z1 = [int(code[4][2]) for code in block] # div z {z[i]}
# then add x which also variate
x1 = [int(code[5][2]) for code in block] # add x {x[i]}
# then perform this block
'''
eql x w # x = int(x == w)
eql x 0 # x = int(x == 0)
mul y 0 # y = 0
add y 25 # y += 25
mul y x # y += x
add y 1 # y += 1
mul z y # z *= y
mul y 0 # y = 0
add y w # y = w
'''
# then add y
y1 = [int(code[15][2]) for code in block] # add y {y[i]}
# lastly, do
'''
mul y x # y *= x
add z y # z += y
'''
# print(z1)
# print(x1)
# print(y1)
# can translate to python as
#i = step, w = inp, z = prev_z
def run(i, w, z):
	x = (z % 26) + x1[i]
	z //= z1[i]
	if x != w: # x = (int(x == w) == 0)
	# in assembly, x is used to multiply with each line after that
	# technically if x == 0 then z remain same (z *= 1 and z += 0)
		z *= 26
		z += w + y1[i]
	return z
# only z is stored to next block
# at the end of program, z must be zero

# kudos to https://www.reddit.com/user/leijurv/
# https://www.reddit.com/r/adventofcode/comments/rnejv5/comment/hps47kk/?utm_source=reddit&utm_medium=web2x&context=3
# idea is to create a circuit breaker to filter z that unlikely to be an answer out
# calculate the maximum acceptable z value at certain index
# in the thread said that z at that digit should not go beyond
# 26 ** len([z for z in z1[current_idx:] if z == 26])
# if z if beyond this value then stop because it's too high and impossible to decrease
limit_z = []
for z_idx in range(len(z1)):
	multiply_amount = len([z for z in z1[z_idx:] if z == 26])
	limit_z.append(26**multiply_amount)
	# limit_z.append(26**(14-z_idx)) # <- this is my guess, it also works miraculously but slower :D
# print(limit_z)
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
	# if len(res) > 0: print(res)
	return res

solutions = search(0, 0)
solutions = list(map(int, solutions))
answer = max(solutions)

# 1st attempt: not working :(
# can't just brute force
# now use just for checking
class ALU():
	def __init__(self) -> None:
		self.input = []
		self.reg = { 'w':0, 'x':0, 'y':0, 'z':0 }
	def process(self, cmd, i1, i2 = None):
		if i2 != None and type(i2) == str:
			if i2.lstrip('-').isdigit():
				val2 = int(i2)
			else: val2 = self.reg[i2]
		if cmd == 'inp':
			input_given = next(i2)
			self.input.append(input_given)
			self.reg[i1] = int(input_given)
		elif cmd == 'add': self.reg[i1] += val2
		elif cmd == 'mul': self.reg[i1] *= val2
		elif cmd == 'div': self.reg[i1] //= val2
		elif cmd == 'mod': self.reg[i1] %= val2
		elif cmd == 'eql': self.reg[i1] = int(self.reg[i1] == val2)
		
	def isValid(self):
		return self.reg['z'] == 0

def solve(program, guess_number, print_reg = False):
	computer = ALU()
	def guesser():
		guess = guess_number
		for ch in guess:
			yield ch
	guess = guesser()
	for line in program:
		if len(line) == 2:
			computer.process(*line, guess)
		else:
			computer.process(*line)
	if print_reg: print(computer.reg)
	return computer.isValid()
assert solve(program, str(answer))
print(answer)
