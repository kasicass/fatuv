# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from common import TestCase
import unittest
import fatuv as uv

class TestPrepare(TestCase):
	def test_prepare(self):
		self.on_prepare_called = 0

		def on_prepare(prepare_handle):
			self.on_prepare_called += 1
			prepare_handle.stop()

		self.prepare = uv.Prepare(self.loop)
		self.prepare.start(on_prepare)

		self.loop.run()

		self.assert_equal(self.on_prepare_called, 1)

	def test_closed(self):
		self.prepare = uv.Prepare(self.loop)
		self.prepare.close()

		self.assert_raises(uv.HandleClosedError, self.prepare.start)
		self.assert_is(self.prepare.stop(), None)

if __name__ == '__main__':
	unittest.main(verbosity=2)

