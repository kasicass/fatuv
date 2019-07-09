# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from common import TestCase
import unittest

import fatuv as uv


class TestTTY(TestCase):
	def test_tty(self):
		try:
			self.tty = uv.TTY(self.loop, sys.stdin.fileno(), True)
			self.assert_true(bool(self.tty.console_size))
			self.tty.set_mode(uv.tty.UV_TTY_MODE_NORMAL)
			uv.tty.reset_mode()
			self.tty.close()
			self.assert_equal(self.tty.console_size, (0, 0))
			self.assert_raises(uv.HandleClosedError, self.tty.set_mode)
		except uv.UVError or ValueError:
			pass

if __name__ == '__main__':
	unittest.main(verbosity=2)

