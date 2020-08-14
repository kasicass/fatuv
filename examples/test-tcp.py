import sys
sys.path.append('.')

import fatuv
import signal

def on_read(client, data, error):
	if data is None:
		print('client closed:', client.getpeername(), 'nread', error)
		client.close()
		clients.remove(client)
		return
	# client.write(data)
	print('recv', data)

def on_connection(server, status):
	print('on_connection')
	client = fatuv.TCP(loop)
	server.accept(client)
	clients.append(client)
	client.start_read(on_read)
	print('client:', client.getpeername())

def signal_cb(handle, signum):
	server.close()
	signal_h.stop()

loop = fatuv.Loop.default_loop()
clients = []

server = fatuv.TCP(loop)
server.bind(("0.0.0.0", 25000))
server.listen(on_connection)

signal_h = fatuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)

print('Run!')
loop.run()
print('Stop!')

