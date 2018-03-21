import time
import sqlite3
import db_tools
import sys
import os
import json

DEV = True 

class Game:

	def __init__(self, cursor):
		self.cursor = cursor
		self.users  = {}
		self.result   = None
		self.max_perc = None
		self.game_id  = None
		self.time     = None

		self.start = False #this is just to make sure we start collecting at first ocsg instead of somewhere in the middle
		self.reset()

	def parse_json(self,data):
	#here we just send the frame depending on the type of json object
	#we only really care about 'opb' and 'occ' objects, which stand for
	#player-bet and player cash-out.
		if data[0] == 'opb':
			for player in self.parse_opb(data[1]):
				self.users[player[0]] = [player[0], player[1], 0, -1]

		elif data[0] == 'occ':
			try:
				for player in self.parse_occ(data[1]):
					self.users[player[0]][2] = player[2]
					self.users[player[0]][3] = player[1]
			except KeyError:
				print("Key error again, not sure whats up" , player[0], self.users.keys())

		elif data[0] == 'oce':
			self.max_perc = self.parse_oce(data[1])[0]
			self.result = round(sum([self.users[user][1]-self.users[user][2] for user in self.users]),2)
			self.commit()
			self.reset()

	def parse_opb(self,data):
		player_dict = []
		for player in data:
			player_dict.append((player['p'], player['w']))

		return player_dict
		
	def parse_occ(self,data):
		player_dict = []
		if type(data) == type(list()):
			for player in data:
				player_dict.append((player['p'], player['a']/100., player['t']))
		else:
			player_dict.append((data['p'], data['a']/100., data['t']))

		return player_dict

	def parse_oce(self,data): #oce means end game
		return tuple([data['c']/100.])

	def set_time(self, new_time):
		self.time = new_time

	def reset(self):
		if DEV: print('\n')

		self.users = {}
		self.result   = None
		self.max_perc = None
		self.game_id  = get_new_id(self.cursor)
		self.time     = time.time()

	def commit(self):
		if DEV: print(self.game_id, self.result, self.max_perc)
		db_tools.insert_into(self.cursor, 'GAMES', (self.game_id, self.time, self.max_perc, self.result))
		for user in self.users.keys(): add_user(self.cursor, user)
		table_name = 'GAME_' + str(self.game_id)
		new_game_table(self.cursor, table_name)
		db_tools.insert_into(self.cursor, table_name, list(self.users.values()))

def setup_default_tables(cursor):
#setup our User, and Games Tables
	db_tools.build_table(cursor, 'USERS', ['id'])
	db_tools.build_table(cursor, 'GAMES', ['game_id', 'time_utc', 'max_percent', 'total_mon'])

def new_game_table(cursor, table_title):
#this one will be used to create our game tables when we get new ones collected
	game_columns = ['user_id', 'bet_value', 'return_value', 'percent_inc']
	db_tools.build_table(cursor, table_title, game_columns)

def get_new_id(cursor):
#use this function to get the next open game_id

	try: 
		return db_tools.select_values(cursor, 'GAMES', 'MAX(game_id)')[0][0] + 1
	except TypeError: 
		return 0

def add_user(cursor, user_id):
	check = db_tools.select_values(cursor, 'USERS', '*', "id = " + user_id)

	if len(check) == 0:
		db_tools.insert_into(cursor, 'USERS', '(' + str(user_id) + ')')

def main():
	
	db    = 'database\magic_db.db'
	sfile = 'frames\\scraped_frames.txt'
	conn  = sqlite3.connect(db)
	curse = conn.cursor()

	setup_default_tables(curse)
	game  = Game(curse)
	try:
		curr_time = db_tools.select_values(curse, 'GAMES', 'MAX(time_utc)')[0][0]
	except:
		curr_time = None

	while True:
		try:
			new_time = '%.6f' % os.path.getmtime(sfile)
			if curr_time != new_time:
				time.sleep(.5) #okay right here idk why I'm sleeping but if I don't I double read data which I dont wont so this works
				curr_time = '%.6f' % os.path.getmtime(sfile)
				if DEV: print('GOT A NEW ONE', new_time)

				with open(sfile, 'rb') as f:
					frames   = [frame.decode("utf-8") for frame in f.readlines()]
					game.set_time(curr_time)
					for frame in frames[1:]:
						data = json.loads(frame)
						game.parse_json(data)
				conn.commit()

			time.sleep(1)

		except PermissionError:
			print('wait a sec while the file dls')
			time.sleep(1)

		except KeyboardInterrupt:
			conn.commit()
			conn.close()
			sys.exit(0)

def test():
	db    = 'database\magic_db.db'
	conn  = sqlite3.connect(db)
	curse = conn.cursor()

	print(db_tools.select_values(curse, 'GAMES', '*'))
	print(db_tools.select_values(curse, 'GAMES_0', '*'))

if __name__ == "__main__":
	
	main()