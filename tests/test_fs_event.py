# -*- coding: utf-8 -*-

import sys
sys.path.append('.')

from common import TestCase
import unittest
import fatuv as uv
import tempfile
import os


class TestFSEvent(TestCase):
	def test_fs_event_change(self):
		def on_event(fs_event, filename, events, status):
			self.assert_equal(status, uv.error.STATUS_SUCCESS)
			self.assert_equal(filename, os.path.basename(self.temp_file.name))
			self.assert_equal(events, uv.fs_event.UV_FS_EVENTS_CHANGE)
			fs_event.close()

		def on_timeout(timer):
			self.temp_file.write(b'x')
			self.temp_file.flush()
			timer.close()

		self.fs_event = uv.FSEvent(self.loop, callback=on_event)
		self.timer = uv.Timer(self.loop)

		with tempfile.NamedTemporaryFile() as temp_file:
			self.temp_file = temp_file
			self.fs_event.path = temp_file.name
			self.fs_event.start()
			self.timer.start(on_timeout,1,0)
			self.loop.run()

	def test_fs_event_rename(self):
		def on_event(fs_event, filename, events, status):
			self.assert_equal(status, uv.error.STATUS_SUCCESS)
			self.assert_equal(filename, os.path.basename(self.temp_file.name))
			self.assert_equal(events, uv.fs_event.UV_FS_EVENTS_RENAME)
			fs_event.close()

		def on_timeout(timer):
			os.rename(self.temp_file.name, self.temp_file.name + '-new-name')
			timer.close()

		self.fs_event = uv.FSEvent(self.loop, callback=on_event)
		self.timer = uv.Timer(self.loop)

		with tempfile.NamedTemporaryFile() as temp_file:
			self.temp_file = temp_file
			self.fs_event.path = temp_file.name
			self.fs_event.start()
			self.timer.start(on_timeout, 1, 0)
			self.loop.run()
			os.rename(self.temp_file.name + '-new-name', self.temp_file.name)

	def test_fs_event_stop(self):
		self.fs_event = uv.FSEvent(self.loop)

		with tempfile.NamedTemporaryFile() as temp_file:
			self.fs_event.path = temp_file.name
			self.fs_event.start()
			self.fs_event.stop()
			self.loop.run()

	def test_closed(self):
		self.fs_event = uv.FSEvent(self.loop)
		self.fs_event.close()

		self.assert_raises(uv.HandleClosedError, self.fs_event.start)
		self.assert_is(self.fs_event.stop(), None)

	def test_path_none(self):
		self.fs_event = uv.FSEvent(self.loop)

		self.assert_raises(uv.error.ArgumentError, self.fs_event.start)


if __name__ == '__main__':
	unittest.main(verbosity=2)

