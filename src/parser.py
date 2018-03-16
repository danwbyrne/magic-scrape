import json
import sys

def parse_opb(data):
	player_dict = []
	for player in data:
		player_dict.append((player['p'], player['w']))

	return player_dict
		
def parse_occ(data):
	player_dict = []
	if type(data) == type(list()):
		for player in data:
			player_dict.append((player['p'], player['a']/100., player['t']))
	else:
		player_dict.append((data['p'], data['a']/100., data['t']))

	return player_dict

def parse_frame(frame):
#here we just send the frame depending on the type of json object
#we only really care about 'opb' and 'occ' objects, which stand for
#player-bet and player cash-out.

	try:
		data = json.loads(frame)

		if data[0] == 'opb':
			return parse_opb(data[1])

		elif data[0] == 'occ':
			return parse_occ(data[1])

		return None

	except json.decoder.JSONDecodeError:
		print('whats happening here\n')
		print(frame)

	except:
		print("Unexpected Error in parse_frame: ", sys.exc_info()[0])
		return None

def parse_frame_file(frame_file):
#here we can parse a whole frame file and return the parsed frame data as a list.

	with open(frame_file, 'rb') as f:
		frames = [frame.decode("utf-8") for frame in f.readlines()]
		for frame in frames:
			print(parse_frame(frame))
		


if __name__ == "__main__":
	parse_frame_file('frames\\scraped_frames.txt')