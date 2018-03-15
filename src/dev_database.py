import sqlite3
import sys

def build_table(cursor, table_name, table_columns):
#will take a connection cursor object and use it to execute a build table command
#table_name is a string, table_columns should be a list or tuple

	try:
		column_strings = '(' + ', '.join(table_columns) + ')'
		cursor.execute('''CREATE TABLE %s %s''' % (table_name, column_strings))

	except sqlite3.OperationalError:
		print("The table <%s> might already exist in this database." % (table_name))

	except:
		print("Unexpected Error: ", sys.exc_info()[0])

def insert_into(cursor, table_name, insert_columns):
#will take a connection cursor object and a table_name and try to insert
#the input column data into the table. You can insert a whole list of column data
#if you use insert_columns as a list, if not it will just do one.

	#try:
	if type(insert_columns) == type(list()):
		foreign_inputs = '(' + ', '.join(['?' for i in range(len(insert_columns[0]))]) + ')'
		cursor.executemany('INSERT INTO %s VALUES %s' % (table_name, foreign_inputs), insert_columns)

	else:
		foreign_inputs = '('+ ', '.join(['?' for i in range(len(insert_columns))]) + ')'
		cursor.execute('INSERT INTO %s VALUES %s' % (table_name, insert_columns))

	#except:
	#	print("Unexpected Error: ", sys.exc_info()[0])

def select_values(cursor, table_name, select_columns, where_clause=False):
#will take a connection cursor object and table_name and column values
#and try and return the selected values, optional where clause
#where clause should just be a string clause. Accepts selected_values as a list or '*'

	try:
		if type(select_columns) == type(list()): select_statement = ','.join(select_columns)
		else: select_statement = select_columns

		if type(where_clause) == type(str()):
			cursor.execute('SELECT %s FROM %s WHERE %s' % (select_statement, table_name, where_clause))

		else:
			cursor.execute('SELECT %s FROM %s' % (select_statement, table_name))

	except:
		print("Unexpected Error: ", sys.exc_info()[0])
