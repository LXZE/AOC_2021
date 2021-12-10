with open('input.txt') as f:
	chunks = list(map(lambda line: line.strip(), f.readlines()))

mapper = {
	'(': ')',
	'[': ']',
	'{': '}',
	'<': '>'
}

error_score = {
	')': 3,
	']': 57,
	'}': 1197,
	'>': 25137
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
	return stack

res = 0
for line in chunks:
	result = validate(line)
	if isinstance(result, list):
		continue
	else:
		res += error_score[result]
print(res)
