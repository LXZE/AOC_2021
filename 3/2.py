report = []
with open('input.txt', 'r') as f:
	report = list(map(lambda l: l.strip(), f.readlines()))

def find_most_common(lst): return max(set(lst), key=lst.count)

def filtering(bin_list, keep_digit):
	for idx in range(len(bin_list[0])):
		if len(bin_list) == 1: break
		check_bit = find_most_common(list(map(lambda l: l[idx], bin_list)))
		if keep_digit == '0': check_bit = '0' if check_bit == '1' else '1'
		new_list = list(filter(lambda l: l[idx] == check_bit, bin_list))
		if len(bin_list) % 2 == 0 and len(new_list) == len(bin_list) // 2:
			new_list = list(filter(lambda l: l[idx] == keep_digit, bin_list))
		bin_list = new_list
	return bin_list

oxygen_list = filtering(report[:], '1')
carbon_list = filtering(report[:], '0')
print(int(oxygen_list[0], 2) * int(carbon_list[0], 2))