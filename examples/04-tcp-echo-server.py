from __future__ import print_function

import signal
import fatuv

def on_read(client, data, error):
	if data is None:
		print('client closed:', client.getpeername())
		client.close()
		clients.remove(client)
		return
	client.write(data)

def on_connection(server, error):
	client = fatuv.TCP(server.loop)
	server.accept(client)
	clients.append(client)
	client.start_read(on_read)
	print('new client from:', client.getpeername())

def signal_cb(handle, signum):
	[c.close() for c in clients]
	signal_h.close()
	server.close()

print("PyUV version %s" % fatuv.__version__)

loop = fatuv.Loop.default_loop()
clients = []

server = fatuv.TCP(loop)
server.bind(("0.0.0.0", 8888))
server.listen(on_connection)

signal_h = fatuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)

loop.run()
print("Stopped!")

