============
magic-scrape
============

.. code:: bash

	pipenv install
	pipenv run python src\scraper.py


db_tools
========

Sort-sort of convienent
-----------------------
my db_tools library right now is just 3 functions that make sql commands for my main database more abstracted and easier to use later when parsing data. I will almost definitely be adding more to this toolkit.

.. code:: python

	import db_tools
	import sqlite3

	db     = 'database\magic_db.db'
	conn   = sqlite3.connect(db)
	cursor = conn.cursor() #cursor is a easily accessed database connection

	#build an example table in our database
	db_tools.build_table(cursor, 'EXAMPLE_TABLE', ['arg1','arg2',...,])

	#insert values into our table
	db_tools.insert_into(cursor, 'EXAMPLE_TABLE', (arg1,arg2,...,))

	#select values from our table with optional where clause
	db_tools.select_values(cursor, 'EXAMPLE_TABLE', '*', 'WHERE foo = bar')

