import websocket

def test_collect():
	socket = websocket.WebSocket()
	socket.connect('wss://csgomagic.com/socket.io/?EIO=3&transport=websocket')

	while True:
		result = socket.recv_frame()
		print(result)


if __name__ == "__main__":
	test_collect()