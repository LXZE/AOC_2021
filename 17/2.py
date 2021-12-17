with open('input.txt') as f:
	line = f.readline().strip()
	tmp = line.split('x=')
	tmp = tmp[1].split(', y=')
	x_range = list(map(int, tmp[0].split('..')))
	y_range = list(map(int, tmp[1].split('..')))

def feasible(pos_x, pos_y, vel_x, vel_y):
	if x_range[0] <= pos_x <= x_range[1] and y_range[0] <= pos_y <= y_range[1]: return True
	if pos_y < y_range[0] or pos_x > x_range[1]: return False
	return feasible(pos_x + vel_x, pos_y + vel_y, 0 if vel_x == 0 else vel_x - 1, vel_y - 1)

res = []
for velx in range(1, x_range[1] + 1):
	for vely in range(y_range[0], 100): # blindly guess, should not go beyond 100
		if feasible(0,0, velx, vely):
			res.append((velx, vely))
print(len(res))
