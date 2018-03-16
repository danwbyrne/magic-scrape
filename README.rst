============
magic-scrape
============

.. code:: bash

	pipenv install
	pipenv run python src\scraper.py


db_tools
========

Sort-of convienent
------------------
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


Frame Grabbing (The Hacky Way)
==============================

Websocket Authentication is Hard
--------------------------------
connecting to the websocket of csgomagic which streams data was my initial endevour, but getting around the steam login turned out to be much more of a challenge than I anticipated. So, through a lot of searching and trial and error I discovered I could write javascript snippets for Chrome Developer Tools that allow me to parse the frame data and save it to a local file when I've collected a full 'games' worth of data. The javascript snippet I edited to my needs from <https://stackoverflow.com/questions/29953531/how-to-save-websocket-frames-in-chrome> is below, and it utilizes the 'console.save()' snippet from <https://bgrins.github.io/devtools-snippets/>.

It should also be noted that this method of getting the frame data for me required setting my default save directory to magic-scrape/frames as well as using a third-party chrome extension called 'Downloads Overwrite Existing Files'.

.. code:: javascript
	// 
	// csgomagic json variables to check what the frame contents are
	var DATA = new String();
	var count = '"onlineCount"';
	var ocsg = '"ocsg"';
	var chat = 'chat';
	var oct = '"oct"';
	var oce = '"oce"';
	var ocs = '"ocs"';


	var BEG = false;

	// This replaces the browser's `webSocketFrameReceived` code with the original code 
	SDK.NetworkDispatcher.prototype.webSocketFrameReceived = function (requestId, time, response) {
	  var networkRequest = this._inflightRequestsById[requestId];
	  if (!networkRequest) return;
	  var frame = response.payloadData;
	  if (BEG == false) {
	    if (frame.indexOf(ocsg) != -1) {
	        BEG = true;
	        DATA = DATA + frame + '\n';
	    }
	  }
	  else {
	    if (frame.indexOf(oce) != -1) {
	        BEG = false;
	        DATA = DATA + frame + '\n';
	        console.save(DATA, 'scraped_frames.txt');
	        DATA = new String();
	    }

	    else if ((frame.indexOf(oct) == -1) && (frame.indexOf(count) == -1) && (frame.indexOf(chat) == -1) && (frame != 3) && (frame.indexOf(ocs) == -1)) {
	        DATA = DATA + frame + '\n';         
	    }
	  }
	  networkRequest.addFrame(response, time, false);
	  networkRequest.responseReceivedTime = time;
	  this._updateNetworkRequest(networkRequest);
	}


How To Run
----------
Using these snippets we can:
	1. Connect to <csgomagic.com> and login to our steam account to get to the full websocket connection.
	2. Open Developer Tools for the site.
	3. Refresh the website to start with a clean websocket connection.
	4. Open Developer Tools for our Developer Tools (ctrl+shift+j)
	5. Run the console.save snippet, followed by our custom saveFrameData snippet.
	6. Watch as the data is collected and saved to our local directory (frames/scraped_frames.txt)

Now to beginning parsing the data and building our database :)