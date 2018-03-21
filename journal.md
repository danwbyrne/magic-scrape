# Place to store my thoughts while I work

-Dependencies
right now the dependicies are: sqlite3 (part of standard library), and websocket

-GOALS

THINGS WE WANT TO CHECK:
	that the distribution of their random generator matches with the real distribution we scrape

	want to see expected values of return, as well as losses. Basically plot everything about the $$ we can

THINGS WE NEED TO DO:
	Basically need to webscrape the site until we have the results of a full 'game', then add the scraped game to our database as a 'GAME', add all 'USERS' to that table, and make a new table for each game in GAMES.


--BIG FIND
	All of the data we want is in a websocket located at 'wss://csgomagic.com/socket.io/?EIO=3&transport=websocket' however if you aren't logged in with steam it only streams you the simple data (just onlineCount data). We need to get through the steam logon issue.


setup situation:
	main file will create a scraper object that it can just pull data from when ready our main loop will be like
	while True:
		scraper.get_new_data() #this will take time to collect and return a response
		(sort data)


	scraper object setup will be in charge of generating dump objects for us to sort in main

3/20/18
We have started getting the data and adding it to our database using the text file method. It is working very well and is almost bugless at this point. Time to start work on analyzing the data. I copied some starter test data as a copy of the database called 'test_db.db' so we'll start setting up plotting operations now.