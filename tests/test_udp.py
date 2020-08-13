# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from common import TestCase
import unittest

import fatuv as uv
import socket

from _fatcore import lib

MULTICAST_ADDRESS = '239.255.0.1'

def interface_addresses():
	if uv.common.is_win32:
		for interface_address in uv.misc.interface_addresses():
			if len(interface_address) > 2:
				continue
			yield interface_address.address[0]
	else:
		yield MULTICAST_ADDRESS


TEST_IPV4 = '127.0.0.1'
TEST_PORT1 = 12345

class TestUDP(TestCase):
	def test_udp(self):
		self.datagram = None

		def on_receive(udp_handle, data, status, address, flags):
			self.datagram = data
			udp_handle.receive_stop()

		server = socket.socket(type=socket.SOCK_DGRAM)
		self.server = uv.UDP(self.loop)
		#self.assert_equal(self.server.family, None)
		self.server.open(server.fileno())
		#self.assert_equal(self.server.family, server.family)
		self.server.bind((TEST_IPV4, TEST_PORT1))
		#self.assert_equal(self.server.sockname, (common.TEST_IPV4, common.TEST_PORT1))
		self.server.receive_start(callback=on_receive)

		self.client = uv.UDP(self.loop)
		self.client.send(b'hello', (TEST_IPV4, TEST_PORT1))

		self.loop.run()

		self.assert_equal(self.datagram, b'hello')

	def test_udp_multicast(self):
		self.clients = []
		self.results = []

		def on_receive(client, data, status, address, flags):
			self.results.append(data)
			client.receive_stop()

		for address in interface_addresses():
			client = uv.UDP(self.loop)
			client.bind((address, TEST_PORT1))
			client.set_membership(MULTICAST_ADDRESS, lib.FATUV_JOIN_GROUP)
			client.set_multicast_ttl(10)
			client.receive_start(on_receive)
			self.clients.append(client)

		self.server = uv.UDP(self.loop)
		self.server.send(b'hello', (MULTICAST_ADDRESS, TEST_PORT1))

		self.loop.run()

		self.assert_equal(self.results, [b'hello'] * len(self.clients))

	def test_udp_multicast_loop(self):
		self.datagram = None

		def on_receive(client, data, status, address, flags):
			self.datagram = data
			client.receive_stop()

		self.server = uv.UDP(self.loop)
		self.server.bind(('0.0.0.0', TEST_PORT1))
		self.server.set_multicast_interface('0.0.0.0')
		self.server.set_membership(MULTICAST_ADDRESS, lib.FATUV_JOIN_GROUP)
		self.server.set_multicast_loop(True)
		self.server.receive_start(on_receive)
		self.server.send(b'hello', (MULTICAST_ADDRESS, TEST_PORT1))

		self.loop.run()

		self.assert_equal(self.datagram, b'hello')

	def test_udp_broadcast(self):
		self.datagram = None

		def on_receive(server, data, status, address, flags):
			self.datagram = data
			server.close()

		self.server = uv.UDP(self.loop)
		self.server.bind(('0.0.0.0', TEST_PORT1))
		self.server.set_broadcast(True)
		self.server.receive_start(on_receive)

		self.client = uv.UDP(self.loop)
		self.client.bind(('0.0.0.0', 0))
		self.client.set_broadcast(True)
		self.client.send(b'hello', ('255.255.255.255', TEST_PORT1))

		self.loop.run()

		self.assert_equal(self.datagram, b'hello')

	def test_udp_try_send(self):
		self.datagram = None

		def on_receive(udp_handle, data, status, address, flags):
			self.datagram = data
			udp_handle.receive_stop()

		def on_timeout(timer):
			try:
				self.client.try_send(b'hello', (TEST_IPV4, TEST_PORT1))
			except uv.error.TemporaryUnavailableError:
				self.server.close()
				self.datagram = b'hello'

		self.server = uv.UDP(self.loop)
		self.server.bind((TEST_IPV4, TEST_PORT1))
		self.server.receive_start(on_receive)

		self.client = uv.UDP(self.loop)
		self.client.bind(('0.0.0.0', 0))

		self.timer = uv.Timer(self.loop)
		self.timer.start(on_timeout,1,0)

		self.loop.run()

		self.assert_equal(self.datagram, b'hello')

	def test_udp_closed(self):
		self.udp = uv.UDP(self.loop)
		self.udp.close()
		#self.assert_is(self.udp.family, None)
		#self.assert_equal(self.udp.sockname, ('0.0.0.0', 0))
		self.assert_raises(uv.HandleClosedError, self.udp.open, None)
		self.assert_raises(uv.HandleClosedError, self.udp.set_membership, None, None)
		self.assert_raises(uv.HandleClosedError, self.udp.set_multicast_loop, False)
		self.assert_raises(uv.HandleClosedError, self.udp.set_multicast_ttl, 10)
		self.assert_raises(uv.HandleClosedError, self.udp.set_multicast_interface, None)
		self.assert_raises(uv.HandleClosedError, self.udp.set_broadcast, False)
		#self.assert_raises(uv.HandleClosedError, self.udp.bind, ('0.0.0.0', 0))
		#self.assert_raises(uv.HandleClosedError, self.udp.send, b'', ('0.0.0.0', 0))
		#self.assert_raises(uv.HandleClosedError, self.udp.try_send, b'', ('0.0.0.0', 0))
		#self.assert_raises(uv.HandleClosedError, self.udp.receive_start)
		#self.assert_is(self.udp.receive_stop(), None)

if __name__ == '__main__':
	unittest.main(verbosity=2)

