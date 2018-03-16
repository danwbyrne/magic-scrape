#x types of data recieved, 'opb', 'ocs', 'oct', 'oce', 'onlineCount', 'occ'
#on 'ocsg' we just know to start a new game table
#on 'oct' we pass
#on 'onlineCount' we pass
#on 'opb' we go through

import json

def parse_opb(data):
	player_dict = []
	for player in data:
		player_dict.append((player['p'], player['w']))

	return player_dict
		
def parse_occ(data):
	player_dict = []
	player_dict.append((data['p'], data['a']/100., data['t']))

	return player_dict

def parse_frame(frame):
	frame = frame[2:]
	data = json.loads(frame)

	try:

		if data[0] == 'opb':
			return parse_opb(data[1])

		elif data[0] == 'occ':
			return parse_occ(data[1])

		elif data[0] == 'ocsg':
			return 'NEW BET PHASE'

		elif data[0] == 'ocs':
			return 'NEW GAME PHASE'

		elif data[0] == 'oce':
			return parse_oce(data[1])

		return None

	except:
		pass
 





if __name__ == "__main__":
	print(parse_frame(test))