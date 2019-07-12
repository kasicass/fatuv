# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from common import TestCase
import unittest
import fatuv as uv
import os
from _fatuv import lib
import json


__dir__ = os.path.dirname(os.path.realpath(__file__))

def resolve_path(relative_path):
	return os.path.join(__dir__, 'data', relative_path)

PROGRAM_HELLO = resolve_path('program_hello.py')
PROGRAM_ENDLESS_LOOP = resolve_path('program_endless_loop.py')
PROGRAM_DUMP_ENV = resolve_path('program_dump_env.py')

TEST_PIPE1 = '/tmp/python-uv-test1'

class TestProcess(TestCase):
	def test_process_hello(self):
		arguments = [sys.executable, PROGRAM_HELLO]
		self.buffer = b''
		self.returncode = None

		def on_exit(process_handle, returncode, term_signal):
			self.returncode = returncode

		def on_read(pipe_handle,data,status):
			if data:
				self.buffer += data

		self.pipe = uv.Pipe(self.loop)
		self.pipe.bind(TEST_PIPE1)

		self.process = uv.Process(self.loop, arguments, stdout=uv.process.PIPE, stdio=[self.pipe],
								  callback=on_exit)
		self.process.stdout.start_read(on_read)

		self.loop.run()

		self.assert_equal(self.buffer.strip(), b'hello')
		self.assert_equal(self.returncode, 1)
		self.assert_not_equal(self.process.pid, None)
		self.assert_raises(uv.error.UVError, self.process.kill)

		self.process.close()

		self.assert_raises(uv.HandleClosedError, self.process.kill)
		with self.should_raise(uv.HandleClosedError):
			pid = self.process.pid

	def test_process_endless_loop(self):
		arguments = [sys.executable, PROGRAM_ENDLESS_LOOP]

		self.returncode = None
		self.term_signal = None

		def on_exit(process_handle, returncode, term_signal):
			self.returncode = returncode
			self.term_signal = term_signal

		def on_prepare(prepare_handle):
			prepare_handle.close()
			self.process.kill()

		self.process = uv.Process(self.loop, arguments, callback=on_exit)
		self.prepare = uv.Prepare(self.loop)
		self.prepare.start(on_prepare)

		self.loop.run()

		self.assert_is_not(self.returncode, None)
		self.assert_is_not(self.term_signal, None)

	def test_process_dump_env(self):
		arguments = [sys.executable, PROGRAM_DUMP_ENV]
		print PROGRAM_DUMP_ENV
		self.buffer = b''
		self.returncode = None

		def on_exit(process_handle, returncode, term_signal):
			self.returncode = returncode

		def on_read(pipe_handle, data, nread):
			if nread > 0:
				self.buffer += data

		env = {'hello': 'world'}
		self.process = uv.Process(self.loop, arguments, env=env, stdout=uv.process.PIPE, callback=on_exit,
								  cwd=resolve_path(''))
		self.process.stdout.start_read(on_read)

		self.loop.run()

		self.assert_equal(self.returncode, 0)
		self.assert_not_equal(self.process.pid, None)

		result = json.loads(self.buffer.decode())
		self.assert_equal(result['hello'], 'world')
		self.assert_true(result['cwd'].endswith('tests/data'))

	def test_unknown_file(self):
		arguments = [sys.executable, PROGRAM_HELLO]
		self.assert_raises(uv.error.ArgumentError, uv.Process, self.loop, arguments, stdout='abc')

if __name__ == '__main__':
	unittest.main(verbosity=2)