ip = input('Enter ip address: ').split('.')
mask = input('Enter mask: ')

net_masks = dict()
okt = {1:8, 2:16, 3:24, 4:32}

def get_oktet(mask):
	if mask < 8:
		oktet = 1
	elif mask < 16:
		oktet = 2
	elif mask < 24:
		oktet = 3
	else:
		oktet = 4

	return oktet

twoInPower = 0
for i in range(0, 33):
	if i < 8:
		power = okt[get_oktet(i)]-i
		if power == 8:
			net_masks['0.0.0.0'] = i
		else:
			twoInPower += 2**power
			net_masks[f'{twoInPower}.0.0.0'] = i
		if i == 7:
			twoInPower = 0
	if i < 16 and i > 7:
		power = okt[get_oktet(i)]-i
		if power == 8:
			net_masks['255.0.0.0'] = i
		else:
			twoInPower += 2**power
			net_masks[f'255.{twoInPower}.0.0'] = i
		if i == 15:
			twoInPower = 0
	if i < 24 and i > 15:
		power = okt[get_oktet(i)]-i
		if power == 8:
			net_masks['255.255.0.0'] = i
		else:
			twoInPower += 2**power
			net_masks[f'255.255.{twoInPower}.0'] = i
		if i == 23:
			twoInPower = 0
	if i < 32 and i > 23:
		power = okt[get_oktet(i)]-i
		if power == 8:
			net_masks['255.255.255.0'] = i
		else:
			twoInPower += 2**power
			net_masks[f'255.255.255.{twoInPower}'] = i
		if i == 31:
			net_masks['255.255.255.255'] = i +1

if len(mask) > 2:
	mask = net_masks[mask]

def calc_range(ip, mask, okt):
	oktet = get_oktet(mask)
	net = None
	power = 2**(okt[oktet] - mask)
	ip_frame = int(ip[oktet-1])
	for i in range(ip_frame, 0, -1):
		if i % power == 0:
			net = i
			break
	if net == None:
		net = 0
	network = []
	broadcast_addr = []
	for i in range(0, oktet-1):
		network.append(str(ip[i]))
	network.append(str(net))
	length = len(network)
	for i in range(4-length):
		network.append('0')
	first_addr = network.copy()
	first_addr[3] = str(int(first_addr[3]) + 1)
	last = net + (power-1)
	for i in range(0, oktet-1):
		broadcast_addr.append(str(ip[i]))
	broadcast_addr.append(str(last))
	while len(broadcast_addr) != 4:
		broadcast_addr.append('255')
	last_addr = broadcast_addr.copy()
	last_addr[3] = str(int(last_addr[3]) -1)
	hosts = 256**(4-oktet) * power -2
	network = '.'.join(network)
	first_addr = '.'.join(first_addr)
	last_addr = '.'.join(last_addr)
	broadcast_addr = '.'.join(broadcast_addr)
	addr_range = f'{network} - {broadcast_addr}'  
	if mask == 32:
		hosts = 1
		first_addr = network
		last_addr = network
		broadcast_addr = '-'
		addr_range = '-'
	elif mask == 31:
		first_addr = '-'
		last_addr = '-'

	print('\nNetwork: ', network, str(f'/{mask}'), sep='')
	print('First address:', first_addr)
	print('Last address:', last_addr)
	print('Broadcast address:', broadcast_addr)
	print('Range:', addr_range)
	print('Amount of hosts:', str(hosts))

calc_range(ip, int(mask), okt)