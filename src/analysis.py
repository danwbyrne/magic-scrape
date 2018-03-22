import sqlite3
import db_tools
import matplotlib.pyplot as plt
import math
import time

#TIME-SERIES ANALYSIS#

def plot_total_revenue(cursor):
	data = db_tools.select_values(cursor, 'GAMES', ['time_utc','total_mon'])
	total = 0
	ts, ys = [], []
	for value in data:
		total += value[1]
		ts.append(time.ctime(float(value[0])))
		ys.append(total)

	plt.axhline()

	plt.plot(ts, ys, 'r+')
	plt.xticks([])
	plt.show()

def plot_histogram_percs(cursor):
	data = db_tools.select_values(cursor, 'GAMES', ['max_percent', 'total_mon'])
	xs   = [point[0] for point in data]
	value_dict = {}
	plt_dict = {}

	for x in xs: value_dict[x] = []
	for point in data: value_dict[point[0]].append(point[1])
	over_hun = []

	for value in value_dict.keys():
		if value >= 100:
			over_hun.append(value_dict[value])
		else:
			n   = len(value_dict[value])
			avg = round(sum(value_dict[value]) / float(n),3)
			value_dict[value] = avg

	for value in value_dict.keys():
		if value < 100:
			plt_dict[value] = value_dict[value]

	n = len(over_hun)
	print(over_hun, type(over_hun))
	avg = round(sum([over[0] for over in over_hun])/float(n),2)
	value_dict[100] = avg

	plt.plot(plt_dict.keys(), plt_dict.values(), 'r+')
	plt.show()

def plot_test(cursor):
	data = db_tools.select_values(cursor, 'GAMES', ['max_percent', 'total_mon'], 'max_percent <= 2.00')
	print(data, '\n', len(data))
	value_dict = {}
	for point in data:
		value_dict[point[0]] = []

	for point in data:
		value_dict[point[0]].append(point[1])

	for value in value_dict.keys():
		n   = len(value_dict[value])
		avg = round(sum(value_dict[value]) / float(n),2)
		value_dict[value] = avg

	plt.plot(value_dict.keys(), value_dict.values(), 'r+')
	plt.axhline()
	plt.show()

def real_max(cursor):
	games = db_tools.select_values(cursor, 'GAMES', 'game_id, max_percent')
	xs = range(len(games))
	ys = []
	zs = []

	for tup in games:
		game_id = tup[0]
		ys.append(tup[1])
		zs.append(db_tools.select_values(cursor, 'GAME_' + str(game_id), 'MAX(percent_inc)')[0][0])

	plt.plot(xs, ys, 'r+')
	plt.plot(xs, zs, 'g+')
	plt.show()

def user_revs(cursor):
	users = dict([(data[0], []) for data in db_tools.select_values(cursor, 'USERS', 'id')])
	games = [data[0] for data in db_tools.select_values(cursor, 'GAMES', 'game_id')]

	for game_id in games:
		data = db_tools.select_values(cursor, 'GAME_' + str(game_id), 'user_id, bet_value, return_value')
		for info in data:
				users[int(info[0])].append(info[2] - info[1])

	for user in users.keys():
		total = round(sum(users[user]),3)
		users[user] = total

	users_pos = dict([(user, users[user]) for user in users.keys() if users[user] > 0])
	users_neg = dict([(user, users[user]) for user in users.keys() if users[user] < 0])
	users_zer = dict([(user, users[user]) for user in users.keys() if users[user] == 0])

	plt.plot(range(len(users_neg.keys())), users_neg.values(), 'r+')
	plt.plot(range(len(users_pos.keys())), users_pos.values(), 'g+')
	plt.plot(range(len(users_zer.keys())), users_zer.values(), 'b-')
	print(len(users_neg.keys()) / len(users.keys()))
	print(sum(users_neg.values()))
	print(sum(users_pos.values()))
	plt.show()

def house_odds(cursor):

	games = [data[0] for data in db_tools.select_values(cursor, 'GAMES', 'game_id')]
	bets  = []
	couts = []

	for game_id in games:
		data = db_tools.select_values(cursor, 'GAME_' + str(game_id), 'bet_value, return_value')
		for user in data:
			bets.append(user[0])
			couts.append(user[1])

	tot_bet = round(sum(bets),3)
	tot_out = round(sum(couts),3)

	print(round(1.-tot_out/tot_bet,4))

def perc_track(cursor):
	data = dict(db_tools.select_values(cursor, 'GAMES', 'time_utc, max_percent'))
	plt.plot(data.keys(), data.values(), 'b.')
	plt.xticks([])
	plt.show()





def main():
	db    = 'database\\test_db.db'
	conn  = sqlite3.connect(db)
	curse = conn.cursor()

	'''plot_total_revenue(curse)
	plot_test(curse)
	user_revs(curse)'''
	perc_track(curse)

	bdate = db_tools.select_values(curse, 'GAMES', 'time_utc','game_id=0')
	edate = db_tools.select_values(curse, 'GAMES', 'MAX(time_utc)')
	print(time.ctime(float(bdate[0][0])))
	print(time.ctime(float(edate[0][0])))


if __name__ == "__main__":
	main()

