from __future__ import print_function
import sys
sys.path.append('.')
sys.path.append('./fatuv')
from fatuv import Loop
from fatuv import dns


def dns_callback(result, error):
	print('error', error)
	print('result:', result)

loop = Loop.default_loop()

dns.getaddrinfo(loop, 'irc.freenode.net', 6667, dns_callback)
#dns.getaddrinfo(loop, 'localhost', 80, dns_callback)
loop.run()

