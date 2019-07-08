# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from common import TestCase
import unittest
import fatuv as uv
import socket

class TestPoll(TestCase):
    def test_poll(self):
        def on_shutdown(stream, _):
            stream.close()

        def on_connection(server, status):
            client = uv.TCP(server.loop)
            server.accept(client)
            client.write(b'hello')
            client.shutdown(callback=on_shutdown)
            server.close()

        self.buffer = b''

        def on_event(poll_handle, status, events):
            if status == uv.error.STATUS_SUCCESS:
                self.buffer = self.client.recv(1024)
            if self.buffer.startswith(b'hello') or status != uv.StatusCodes.SUCCESS:
                poll_handle.stop()

        self.tcp = uv.TCP(self.loop)
        self.tcp.bind(('127.0.0.1', 12345))
        self.tcp.listen(on_connection)

        self.client = socket.socket()
        self.client.connect(('127.0.0.1', 12345))

        self.poll = uv.Poll(self.loop, self.client.fileno(), callback=on_event)
        self.poll.start()

        self.assert_equal(self.poll.fileno(), self.client.fileno())

        self.loop.run()

        self.assert_equal(self.buffer, b'hello')

    def test_closed(self):
        self.client = socket.socket()
        self.poll = uv.Poll(self.loop, self.client.fileno())
        self.poll.close()

        self.assert_raises(uv.HandleClosedError, self.poll.start)
        self.assert_is(self.poll.stop(), None)

if __name__ == '__main__':
	unittest.main(verbosity=2)