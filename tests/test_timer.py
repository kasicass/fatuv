# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from common import TestCase
import unittest
import fatuv as uv


class TestTimer(TestCase):
	def test_timer_simple(self):
		self.timer_called = 0

		def on_timeout(_):
			self.timer_called += 1
			print self.timer_called

		timer = uv.Timer(self.loop)
		timer.start(on_timeout, 1, 0)

		self.loop.run()

		self.assert_equal(self.timer_called, 1)

	def test_timer_repeat(self):
		self.timer_called = 0

		def on_timeout(t):
			self.timer_called += 1
			if self.timer_called == 3:
				t.close()

		timer = uv.Timer(self.loop)
		timer.start(on_timeout, 2, 2)

		self.loop.run()

		self.assert_equal(self.timer_called, 3)

	def test_timer_close(self):
		self.timer_called = 0

		def on_timeout(_):
			self.timer_called += 1

		timer = uv.Timer(self.loop)
		timer.start(on_timeout, 5, 0)
		timer.close()

		self.loop.run()

		self.assert_equal(self.timer_called, 0)

	def test_timer_reference(self):
		self.timer_called = 0

		def on_timeout(_):
			self.timer_called += 1

		timer = uv.Timer(self.loop)
		timer.start(on_timeout, 5, 0)
		timer.dereference()

		self.loop.run()
		self.assert_false(timer.referenced)
		self.assert_equal(self.timer_called, 0)

		timer.reference()

		self.loop.run()

		self.assert_true(timer.referenced)
		self.assert_equal(self.timer_called, 1)

	def test_closed(self):
		self.timer = uv.Timer(self.loop)
		self.timer.close()

		try:
			repeat = self.timer.repeat
		except uv.HandleClosedError:
			pass
		else:
			self.assert_true(False)
		try:
			self.timer.repeat = 10
		except uv.HandleClosedError:
			pass
		else:
			self.assert_true(False)
		self.assert_raises(uv.HandleClosedError, self.timer.again)
		self.assert_raises(uv.HandleClosedError, self.timer.start, None, 10, 0)
		self.assert_is(self.timer.stop(), None)


if __name__ == '__main__':
	unittest.main(verbosity=2)

