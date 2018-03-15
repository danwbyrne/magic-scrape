from bs4 import BeautifulSoup
import sqlite3
import dev_database

def setup_default_tables(cursor):
#setup our User, and Games Tables
	dev_database.build_table(cursor, 'USERS', ['id', 'games_ids'])
	dev_database.build_table(cursor, 'GAMES', ['game_id', 'time_utc'])

def new_game_table(cursor, game_id):
	pass


def main():
	db = 'test_db.db'
	conn  = sqlite3.connect(db)
	curse = conn.cursor()

	test_info = [(12, '12'), (14,'14')]
	dev_database.insert_into(curse, 'GAMES', test_info)

	dev_database.select_values(curse, 'GAMES', '*', where_clause='game_id = 12')
	print(curse.fetchall())

if __name__ == "__main__":
	
	main()