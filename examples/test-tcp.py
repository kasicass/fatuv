import sys
sys.path.append('.')

import fatuv
import signal

def on_connection(server, status):
	print 'on_connection'
	client = fatuv.TCP(loop)
	server.accept(client)
	print 'client:', client.getpeername()

def signal_cb(handle, signum):
	server.close()
	signal_h.stop()

loop = fatuv.Loop.default_loop()

server = fatuv.TCP(loop)
server.bind(("0.0.0.0", 25000))
server.listen(on_connection)

signal_h = fatuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)

print 'Run!'
loop.run()
print 'Stop!'

