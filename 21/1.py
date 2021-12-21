input_file = 'input'
with open(f'{input_file}.txt') as f:
	p1_pos = int(f.readline().strip()[-1])
	p2_pos = int(f.readline().strip()[-1])

class Dice():
	def __init__(self):
		self.val = 0
		self.count = 0
	def roll(self):
		self.count += 1
		self.val += 1
		if self.val > 100:
			self.val = 1
		return self.val

dice = Dice()
players_pos = [p1_pos, p2_pos]
players_score = [0,0]
loser = 0
turn = 0
while True:
	if any(score >= 1000 for score in players_score):
		loser = min(*players_score)
		break
	move_amount = [dice.roll() for _ in range(3)]
	players_pos[turn] += sum(move_amount)
	# print(f'player{turn+1} rolled {move_amount}')
	if players_pos[turn] > 10:
		# print('minus', players_pos[turn])
		# keep player in range 1-10
		players_pos[turn] = players_pos[turn] % 10
		if players_pos[turn] == 0:
			players_pos[turn] = 10

	players_score[turn] += players_pos[turn]
	turn = (turn + 1) % 2
	# print(players_pos, players_score)
print(loser * dice.count)
