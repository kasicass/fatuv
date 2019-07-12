# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from common import TestCase
import unittest
import fatuv as uv

TEST_PIPE1 = '/tmp/python-uv-test1'

class TestStream(TestCase):
	def test_closed(self):
		self.pipe = uv.Pipe(self.loop)
		self.pipe.close()
		self.assert_false(self.pipe.readable)
		self.assert_false(self.pipe.writable)
		self.assert_raises(uv.HandleClosedError, self.pipe.shutdown)
		self.assert_raises(uv.HandleClosedError, self.pipe.listen, None)
		self.assert_raises(uv.HandleClosedError, self.pipe.start_read,None)
		self.assert_is(self.pipe.stop_read(), None)
		self.assert_raises(uv.HandleClosedError, self.pipe.write, b'')
		self.assert_raises(uv.HandleClosedError, self.pipe.try_write, b'')
		self.assert_raises(uv.HandleClosedError, self.pipe.accept, None)

	def test_try_write(self):
		self.buffer = b''
		self.bytes_written = 0

		def on_read(connection, data, status):
			self.buffer += data
			connection.stop_read()

		def on_connection(pipe_handle, status):
			client = uv.Pipe(pipe_handle.loop)
			pipe_handle.accept(client)
			client.start_read(on_read)
			pipe_handle.close()

		def on_timeout(timer):
			try:
				self.bytes_written = self.client.try_write(b'hello')
			except uv.error.TemporaryUnavailableError:
				self.server.close()
			finally:
				timer.close()

		self.server = uv.Pipe(self.loop)
		self.server.bind(TEST_PIPE1)
		self.server.listen(on_connection)

		self.client = uv.Pipe(self.loop)
		self.client.connect(TEST_PIPE1)

		self.timer = uv.Timer(self.loop)
		self.timer.start(on_timeout,1,0)

		self.loop.run()

		self.assert_equal(self.buffer, b'hello'[:self.bytes_written])

	def test_writable_readable(self):
		self.pipe = uv.Pipe(self.loop)
		self.assert_false(self.pipe.readable)
		self.assert_false(self.pipe.writable)


if __name__ == '__main__':
	unittest.main(verbosity=2)