from collections import defaultdict as ddict
from functools import lru_cache
from pprint import pprint

input_file = 'input'
with open(f'{input_file}.txt') as f:
	p1_pos = int(f.readline().strip()[-1])
	p2_pos = int(f.readline().strip()[-1])

# calc {amount of score: appearance} from each 3 toss * 3 splited universe
toss = {k: 0 for k in range(3,10)}
for i in range(1,4):
	for j in range(1,4):
		for k in range(1,4):
			toss[i+j+k] += 1

@lru_cache(maxsize=None)
def get_score(pos, prev_score):
	return prev_score + 10 if pos == 0 else prev_score + pos

# state_info = (p1, p2, s1, s2)
def calc(current_player, given_state, states_info, appear_count):
	for roll, times in toss.items():
		if current_player == 0:
			new_pos = (states_info[0] + roll) % 10
			new_score = get_score(new_pos, states_info[2])
			given_state[(new_pos, states_info[1], new_score, states_info[3])] += appear_count * times 
		else:
			new_pos = (states_info[1] + roll) % 10
			new_score = get_score(new_pos, states_info[3])
			given_state[(states_info[0], new_pos, states_info[2], new_score)] += appear_count * times 

limit_score = 21
states = {(p1_pos, p2_pos, 0, 0): 1}
turn = 0

while True:
	new_states = ddict(int)
	for (p1,p2,s1,s2), val in states.items():
		if s1 < limit_score and s2 < limit_score:
			calc(turn, new_states, (p1,p2,s1,s2), val)
		else:
			# keep states if one of the players has won
			new_states[(p1,p2,s1,s2)] += val
	states = new_states
	turn = (turn + 1) % 2

	# print(f'Player {turn+1} move')
	# pprint(states)
	complete = True
	for p1,p2,s1,s2 in states.keys():
		if s1 < limit_score and s2 < limit_score:
			# print('not complete yet')
			# print(f'at {p1},{p2},{s1},{s2}')
			complete = False
			break
	if complete:
		break
# pprint(states)
wins = [0,0]
for (p1,p2,s1,s2), val in states.items():
	if s1 >= limit_score:
		assert s1 > s2
		wins[0] += val
	else :
		assert s1 < s2
		wins[1] += val
print(max(wins))
