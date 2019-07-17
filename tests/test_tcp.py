# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from common import TestCase
import unittest
import fatuv as uv
import socket

TEST_IPV4 = '127.0.0.1'
TEST_PORT1 = 12345

class TestTCP(TestCase):
	def test_closed(self):
		self.tcp = uv.TCP(self.loop)
		self.tcp.close()

		self.assert_raises(uv.HandleClosedError, self.tcp.open, 0)
		self.assert_raises(uv.HandleClosedError, self.tcp.bind, None)
		self.assert_raises(uv.HandleClosedError, self.tcp.connect, (TEST_IPV4, 42),None)
		# with self.should_raise(uv.HandleClosedError):
		# 	sockname = self.tcp.sockname
		# with self.should_raise(uv.HandleClosedError):
		# 	peername = self.tcp.peername
		self.assert_raises(uv.HandleClosedError, self.tcp.nodelay, True)
		self.assert_raises(uv.HandleClosedError, self.tcp.keepalive, True, 10)
		self.assert_raises(uv.HandleClosedError, self.tcp.set_simultaneous_accepts, True)

	def test_settings(self):
		self.tcp = uv.TCP(self.loop)
		self.tcp.nodelay(True)
		self.tcp.keepalive(False, 10)
		self.tcp.set_simultaneous_accepts(True)

	def test_open(self):
		server = socket.socket()
		self.tcp = uv.TCP(self.loop)
		self.tcp.open(server.fileno())

	# def test_family(self):
	# 	self.tcp4 = uv.TCP(self.loop)
	# 	self.assert_equal(self.tcp4.family, None)
	# 	self.tcp4.bind((TEST_IPV4, TEST_PORT1))
	# 	self.assert_equal(self.tcp4.family, socket.AF_INET)

	# 	self.tcp6 = uv.TCP(self.loop)
	# 	self.tcp6.bind((TEST_IPV6, TEST_PORT1))
	# 	self.assert_equal(self.tcp6.family, socket.AF_INET6)

	def test_sockname_peername(self):
		address = (TEST_IPV4, TEST_PORT1)

		def on_connection(server, status):
			server.close()

		def on_connect(stream, status):
			# self.assert_equal(request.stream.peername, address)
			stream.close()

		self.server = uv.TCP(self.loop)
		self.server.bind(address)
		self.server.listen(on_connection)
		# self.assert_equal(self.server.sockname, address)

		self.client = uv.TCP(self.loop)
		self.client.connect(TEST_IPV4,TEST_PORT1, callback=on_connect)

		self.loop.run()


if __name__ == '__main__':
	unittest.main(verbosity=2)

