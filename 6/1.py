with open('input.txt') as f:
	states = list(map(int, f.readline().strip().split(',')))
# print(states)

for day in range(80):
	new_fish = states.count(0)
	states = list(map(lambda x: 6 if x == 0 else x - 1, states))
	states.extend([8] * new_fish)
print(len(states))
