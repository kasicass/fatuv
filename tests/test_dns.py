# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from common import TestCase
import unittest
import fatuv as uv
from fatuv import dns

TEST_IPV4 = '127.0.0.1'
TEST_PORT1 = 12345


class TestDNS(TestCase):
	def test_dns_async(self):
		def got_addrinfo(request, code, addrinfo):
			self.assert_true(addrinfo)

		#def got_nameinfo(request, code, hostname, service):
		#	self.assert_equal(service, 'http')

		dns.getaddrinfo('localhost', 80, callback=got_addrinfo)
		#uv.getnameinfo('127.0.0.1', 80, callback=got_nameinfo)

		self.loop.run()

	def test_structures(self):
		address4 = dns.Address4(TEST_IPV4, TEST_PORT1)
		self.assert_equal(address4.host, TEST_IPV4)
		self.assert_equal(address4.port, TEST_PORT1)

		#nameinfo = uv.NameInfo('localhost', 'http')
		#self.assert_equal(nameinfo.hostname, 'localhost')
		#self.assert_equal(nameinfo.service, 'http')

		addrinfo = dns.AddrInfo(0, 1, 2, None, address4)
		self.assert_equal(addrinfo.family, 0)
		self.assert_equal(addrinfo.socktype, 1)
		self.assert_equal(addrinfo.protocol, 2)
		self.assert_is(addrinfo.canonname, None)
		self.assert_equal(addrinfo.address, address4)

if __name__ == '__main__':
	unittest.main(verbosity=2)