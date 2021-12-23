import re
from functools import lru_cache
from pprint import pprint
from typing import Tuple

input_file = 'input'
with open(f'{input_file}.txt') as f:
	f.readline(); f.readline();
	data = re.findall(r'[A-D]', f.readline().strip())
	data.extend(re.findall(r'[A-D]', f.readline().strip()))

def lst2tup(lst):
	return tuple([tuple(e) if type(e) == list else e for e in lst])

def tup2lst(tup):
	return [list(e) if type(e) == tuple else e for e in tup]

rooms = tuple([(data[i+4], data[i]) for i in range(0, 4)])
room_size = 2
final_state = lst2tup([['A'] * room_size, ['B'] * room_size, ['C'] * room_size, ['D'] * room_size])
target_room = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
avaliable_hall_position = [i for i in range(0, 11) if i not in target_room.values()]
cost_by_type = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

def can_enter_room(states, hallway, pod_position):
	pod_to_move = hallway[pod_position]
	target_room_idx = target_room[pod_to_move]
	room_mate = states[(target_room_idx // 2) - 1]
	tmp_hallway = tup2lst(hallway)
	# remove pod at current position in hall way first
	# so it won't count itself as a blockage
	tmp_hallway[pod_position] = None
	if all(pod_in_hallway == None # check if no blockage on the way to room
		for pod_in_hallway in tmp_hallway[
			min(target_room_idx, pod_position):
			max(target_room_idx, pod_position) + 1
		]):
		# check if target room is valid to enter
		if len(room_mate) == 0:
			return True # if room is empty = go in
		for mate in room_mate: # if room is not empty = check pod roommate in the room
			if mate != pod_to_move:
				return False # if wrong pod in room = can't enter
		return True
	return False

def solve(states):
	@lru_cache(maxsize=None) # need to change all params to tuple because of this
	def calculate(hallway: Tuple[str, None], rooms: Tuple[Tuple[str]]):
		# print('current is')
		# pprint(hallway)
		# pprint(rooms)
		if rooms == final_state: return 0
		best_cost = float('inf')
		for idx_pod, current_pod in enumerate(hallway): # move hallway pod to room
			if current_pod is None: continue
			if can_enter_room(rooms, hallway, idx_pod):
				target_room_idx = (target_room[current_pod] // 2) - 1
				new_hallway = hallway[:idx_pod] + (None,) + hallway[idx_pod + 1:]
				new_rooms = tup2lst(rooms)
				new_rooms[target_room_idx].append(current_pod)
				distance = abs(target_room[current_pod] - idx_pod)
				distance += 3 - len(new_rooms[target_room_idx]) # required step to get into room
				cost = distance * cost_by_type[current_pod]
				# pprint(new_hallway)
				# pprint(new_rooms)
				# print(cost)
				# this will eliminate the blockage on the hallway til it can't move anymore
				# and find further moves with for loop beneath
				best_cost = min(best_cost, cost + calculate(new_hallway, lst2tup(new_rooms)))
		
		# try moving pod in the wrong room
		# or wrong arrangement to somewhere else in hallway
		# if pod in room == 0: continue
		# if pod in room == 1:
		# 	if pod type in room == pod type: continue
		# if pod in room == 2:
		# 	if pod == right, right = continue
		# 	else pop
		for idx_room, pods_in_room in enumerate(rooms):
			if len(pods_in_room) == 0 \
				or pods_in_room == final_state[idx_room] \
				or (len(pods_in_room) == 1 and pods_in_room[0] == final_state[idx_room][0]): continue
			else:
				candidate_pod = pods_in_room[-1]
				current_room_position = (idx_room + 1) * 2
				for hall_position in avaliable_hall_position:
					if all(pod_in_hallway == None
						for pod_in_hallway in hallway[
							min(current_room_position, hall_position):
							max(current_room_position, hall_position) + 1
						]):
						new_hallway = hallway[:hall_position] + (candidate_pod,) + hallway[hall_position + 1:]
						new_rooms = tup2lst(rooms)
						new_rooms[idx_room].pop()
						distance = abs(hall_position - current_room_position)
						distance += 2 - len(new_rooms[idx_room]) # required step to get out the room
						cost = distance * cost_by_type[candidate_pod]
						# pprint(new_hallway)
						# pprint(new_rooms)
						# print(cost)
						best_cost = min(best_cost, cost + calculate(new_hallway, lst2tup(new_rooms)))
		return best_cost
	return calculate(tuple([None] * 11), states)
res = solve(rooms)
print(res)
