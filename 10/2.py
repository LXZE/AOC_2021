with open('input.txt') as f:
	chunks = list(map(lambda line: line.strip(), f.readlines()))

mapper = {
	'(': ')',
	'[': ']',
	'{': '}',
	'<': '>'
}

error_score = {
	')': 1,
	']': 2,
	'}': 3,
	'>': 4,
}

def validate(line):
	stack = []
	for ch in line:
		if ch in ['(', '[', '{', '<']:
			stack.append(ch)
		elif ch in [')', ']', '}', '>']:
			expect = mapper[stack.pop()]
			if ch != expect:
				return ch
	return list(map(lambda item: mapper[item], stack[::-1]))

def score(line):
	res = 0
	for ch in line:
		res *= 5
		res += error_score[ch]
	return res

res = []
for line in chunks:
	result = validate(line)
	if isinstance(result, list):
		res.append(score(result))
	else:
		continue
print(sorted(res)[(len(res) - 1)//2])
