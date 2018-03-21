import sqlite3
import db_tools
import matplotlib.pyplot as plt

#TIME-SERIES ANALYSIS#

def plot_total_revenue(cursor):
	data = db_tools.select_values(cursor, 'GAMES', ['time_utc','total_mon'])
	total = 0
	ts, ys = [], []
	for value in data:
		total += value[1]
		ts.append(value[0])
		ys.append(total)

	plt.axhline()
	plt.plot(ts, ys, 'r+')
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
		avg = round(sum(value_dict[value]) / float(n),3)
		value_dict[value] = avg

	plt.plot(value_dict.keys(), value_dict.values(), 'r+')
	plt.axhline()
	plt.show()




def main():
	db    = 'database\\test_db.db'
	conn  = sqlite3.connect(db)
	curse = conn.cursor()

	#plot_total_revenue(curse)
	#plot_histogram_percs(curse)
	plot_test(curse)
if __name__ == "__main__":
	main()

