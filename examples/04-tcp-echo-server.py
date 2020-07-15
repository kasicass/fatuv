from __future__ import print_function
import sys
sys.path.append('.')
# try:
# 	from http_parser.parser import HttpParser
# except ImportError:
# 	from http_parser.pyparser import HttpParser

import signal
import fatuv

PAYLOAD_LEN_EXT16 = 0x7e

# p=HttpParser()
body = []
def on_read(client, data, error):
	if data is None:
		print('client closed:', client.getpeername())
		client.close()
		clients.remove(client)
		return
	print('on_read',data)
	client.write(data)
	# recved = len(data)
	# nparsed = p.execute(data,recved)
	# assert nparsed == recved

	# if p.is_headers_complete():
	# 	print(p.get_headers())

	# if p.is_partial_body():
	# 	body.append(p.recv_body())

	# if p.is_message_complete():
	# 	print('is_message_complete')

	# print(body)

	# header = bytearray()
	# header.append(PAYLOAD_LEN_EXT16)
	# client.write(bytes(header))

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

print("FatUV version", fatuv.__version__)

loop = fatuv.Loop.default_loop()
clients = []

server = fatuv.TCP(loop)
server.bind(("0.0.0.0", 25000))
server.listen(on_connection)

signal_h = fatuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)

loop.run()
print("Stopped!")

