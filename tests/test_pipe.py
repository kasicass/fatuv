# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from common import TestCase
import unittest
import socket
import fatuv as uv

from _fatuv import lib

BAD_PIPE = '/path/socket/notexist'
TEST_PIPE1 = '/tmp/python-uv-test1'
TEST_PIPE2 = '/tmp/python-uv-test2'

class TestPipe(TestCase):
    def test_connect_bad(self):
        def on_connect(stream, status):
            self.assert_not_equal(status, uv.error.STATUS_SUCCESS)
            stream.close()

        self.pipe = uv.Pipe(self.loop)
        self.pipe.connect(BAD_PIPE, callback=on_connect)

        self.loop.run()

    def test_sockname(self):
        self.pipe = uv.Pipe(self.loop)
        self.pipe.bind(TEST_PIPE1)
        #self.assert_equal(self.pipe.sockname, TEST_PIPE1)

    def test_peername(self):
        def on_connect(stream, status):
            self.assert_equal(status, uv.error.STATUS_SUCCESS)
            #self.assert_equal(request.stream.peername, TEST_PIPE1)
            stream.close()

        def on_connection(handle, status):
            self.assert_equal(status, uv.error.STATUS_SUCCESS)
            handle.close()

        self.pipe1 = uv.Pipe(self.loop)
        self.pipe1.bind(TEST_PIPE1)
        self.pipe1.listen(on_connection)

        self.pipe2 = uv.Pipe(self.loop)
        self.pipe2.connect(TEST_PIPE1, callback=on_connect)

        self.loop.run()

    def test_no_pending_accept(self):
        self.pipe = uv.Pipe(self.loop)
        #self.assert_raises(uv.error.ArgumentError, self.pipe.pending_accept)

    def test_closed(self):
        self.pipe = uv.Pipe(self.loop)
        self.pipe.close()

        self.assert_raises(uv.error.HandleError, self.pipe.open, 0)
        self.assert_equal(self.pipe.pending_count, 0)
        self.assert_equal(self.pipe.pending_type, None)
        #self.assert_raises(uv.error.HandleClosedError, self.pipe.pending_accept)
        self.assert_raises(uv.error.HandleClosedError, self.pipe.pending_instances, 100)
        #with self.should_raise(uv.error.HandleClosedError):
        #    sockname = self.pipe.sockname
        #with self.should_raise(uv.error.HandleClosedError):
        #    peername = self.pipe.peername
        self.assert_raises(uv.error.HandleClosedError, self.pipe.bind, '')
        self.assert_raises(uv.error.HandleClosedError, self.pipe.connect, '')

    def test_family(self):
        self.pipe = uv.Pipe(self.loop)
        #self.assert_is(self.pipe.family, socket.AF_UNIX)

    def test_pipe_open(self):
        unix_socket = socket.socket(family=socket.AF_UNIX)
        self.pipe = uv.Pipe(self.loop)
        self.pipe.open(unix_socket.fileno())
        self.assert_equal(self.pipe.fileno(), unix_socket.fileno())

if __name__ == '__main__':
	unittest.main(verbosity=2)