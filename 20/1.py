from copy import deepcopy
from itertools import product

input_file = 'input'
with open(f'{input_file}.txt') as f:
	algo = f.readline().strip()
	f.readline()
	image = list(map(lambda line: list(line.strip()), f.readlines()))

assert len(algo) == 512

border = 2
def expand_image(image, is_border_hashtag):
	ch = '#' if is_border_hashtag else '.'
	w = len(image[0]) + (2*border)
	res = []
	for _ in range(border): res.append(ch * w)
	for row in image:
		res.append((ch * border) + ''.join(row) + (ch * border))
	for _ in range(border): res.append(ch * w)
	return list(map(list, res))

def print_image(image):
	for row in image:
		print(''.join(row))

consider_range = [x for x in product(range(-1, 2), repeat=2)]

def solve(image, is_border_hashtag):
	image = expand_image(image, is_border_hashtag)
	# print('original')
	# print_image(image)
	new_image = deepcopy(image)
	for row in range(1, len(image) - 1):
		for col in range(1, len(image[row]) - 1):
			pixels_data = []
			for dr, dc in consider_range:
				# print(f'row {row}, col {col}, dr {dr}, dc {dc}')
				if row + dr < 0 or row + dr >= len(image) or col + dc < 0 or col + dc >= len(image[row]):
					pixels_data.append('0')
				else: pixels_data.append(str(int(image[row + dr][col + dc] == '#')))
			# print(pixels_data, int(''.join(pixels_data), 2))
			new_image[row][col] = algo[int(''.join(pixels_data), 2)]
	image = new_image
	image = image[1:-1]
	for row in image:
		row.pop(0)
		row.pop()
	# print('modified')
	# print_image(image)
	# print('-'*50)
	return image

def calc(image):
	res = 0
	for row in image:
		res += row.count('#')
	return res

step = 2
for i in range(step):
	image = solve(image, i % 2 != 0 if input_file == 'input' else False)
	print_image(image)
print(calc(image))
