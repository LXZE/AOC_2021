report = []
with open('input.txt', 'r') as f:
	report = list(map(lambda l: l.strip(), f.readlines()))

report = list(map(list, zip(*report)))
def most_common(lst): return max(set(lst), key=lst.count)
gamma = list(map(most_common, report))
epsil = list(map(lambda bit: '0' if bit == '1' else '1', gamma))
gamma = ''.join(gamma)
epsil = ''.join(epsil)
print(int(gamma, 2) * int(epsil, 2))