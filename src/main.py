import time
import sqlite3
import db_tools
import sys

def setup_default_tables(cursor):
#setup our User, and Games Tables
	db_tools.build_table(cursor, 'USERS', ['id', 'games_ids'])
	db_tools.build_table(cursor, 'GAMES', ['game_id', 'max_percent', 'time_utc'])

def new_game_table(cursor):
#this one will be used to create our game tables when we get new ones collected
	game_id = get_new_id(cursor)
	game_columns = ['user_id', 'bet_value', 'return_value', 'percent_inc']
	table_title  = 'GAME_' + str(game_id)

	db_tools.build_table(cursor, table_title, game_columns)

def get_new_id(cursor):
#use this function to get the next open game_id
	try: 
		return db_tools.select_values(cursor, 'GAMES', 'MAX(game_id)')[0][0] + 1
	except TypeError: 
		return 0
	except: 
		print("Unexpected Error: ", sys.exc_info()[0])

def main():
	
	db    = 'database\magic_db.db'
	conn  = sqlite3.connect(db)
	curse = conn.cursor()

	setup_default_tables(curse)

if __name__ == "__main__":
	
	main()