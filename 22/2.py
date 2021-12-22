import re
from pprint import pprint

input_file = 'input'
with open(f'{input_file}.txt') as f:
	cmd = []
	steps = []
	for line in f.readlines():
		c, l = line.strip().split(' ')
		cmd.append(c)
		l = tuple(map(int, re.findall(r'-?\d+', l)))
		steps.append(l)

# data = (x1,x2,y1,y2,z1,z2)
def intersect(a, b):
	x1 = max(a[0], b[0]); y1 = max(a[2], b[2]); z1 = max(a[4], b[4]) 
	x2 = min(a[1], b[1]); y2 = min(a[3], b[3]); z2 = min(a[5], b[5])
	if x1 <= x2 and y1 <= y2 and z1 <= z2:
		return (x1, x2, y1, y2, z1, z2)

def size(x1,x2,y1,y2,z1,z2):
	return (x2-x1+1) * (y2-y1+1) * (z2-z1+1)

class Cube():
	def __init__(self, edge) -> None:
		self.edge = edge
		self.removed = []
	def remove_intersect(self, edge):
		intersected = intersect(self.edge, edge)
		if not intersected: return
		# fucking tricky part
		# can't just remove part of cube without thinking that
		# the removed part could be in added back partially
		# Eric you tricky bastard
		for removed_cube in self.removed:
			removed_cube.remove_intersect(intersected)
		self.removed.append(Cube(intersected))
	def volume(self):
		return size(*self.edge) - sum(removed.volume() for removed in self.removed)

cubes = []
for c, s in zip(cmd, steps):
	for cube in cubes:
		cube.remove_intersect(s)
	if c == 'on': cubes.append(Cube(s))

print(sum(cube.volume() for cube in cubes))
