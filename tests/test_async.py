# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from common import TestCase
import unittest
import fatuv as uv
import threading


class TestAsync(TestCase):
	def test_async(self):
		def thread():
			while True:
				with self.lock:
					if self.async_callback_called == 3:
						break
					self.async.send()

		def on_closed(_):
			self.close_callback_called += 1

		def on_wakeup(async):
			with self.lock:
				self.async_callback_called += 1
				if self.async_callback_called == 3:
					async.close(on_closed)
			self.assert_equal(self.loop_thread, threading.current_thread)

		def on_prepare(prepare):
			threading.Thread(target=thread).start()
			prepare.close(on_closed)

		self.async_callback_called = 0
		self.close_callback_called = 0
		self.lock = threading.RLock()

		self.loop_thread = threading.current_thread

		self.async = uv.Async(self.loop, on_wakeup)

		self.prepare = uv.Prepare(self.loop)
		self.prepare.start(on_prepare)

		self.loop.run()

		self.assert_equal(self.async_callback_called, 3)
		self.assert_equal(self.close_callback_called, 2)

	def test_closed(self):
		self.async = uv.Async(self.loop)
		self.async.close()

		self.assert_raises(uv.HandleClosedError, self.async.send)

if __name__ == '__main__':
	unittest.main(verbosity=2)

