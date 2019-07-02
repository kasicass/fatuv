# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from common import TestCase
import unittest
import fatuv as uv
import tempfile
import os
U_TIME = (4200, 4200)


class TestFSPoll(TestCase):
    def test_fs_poll_change(self):
        def on_change(fs_poll, status, previous_stat, current_stat):
            #self.assert_not_equal(previous_stat.mtim, current_stat.mtim) #TODO
            self.assert_equal(status, uv.error.STATUS_SUCCESS)
            fs_poll.close()

        def on_timeout(timer):
            os.utime(self.temp_file.name, U_TIME)
            timer.close()

        self.fs_poll = uv.FSPoll(self.loop, interval=2000, callback=on_change)
        self.timer = uv.Timer(self.loop)

        with tempfile.NamedTemporaryFile() as temp_file:
            self.temp_file = temp_file
            self.fs_poll.path = temp_file.name
            self.fs_poll.start()
            self.timer.start(on_timeout,1,0)
            self.loop.run()

    def test_fs_poll_stop(self):
        self.fs_poll = uv.FSPoll(self.loop)

        with tempfile.NamedTemporaryFile() as temp_file:
            self.fs_poll.path = temp_file.name
            self.fs_poll.start()
            self.fs_poll.stop()
            self.loop.run()

    def test_closed(self):
        self.fs_poll = uv.FSPoll(self.loop)
        self.fs_poll.close()

        self.assert_raises(uv.HandleClosedError, self.fs_poll.start)
        self.assert_is(self.fs_poll.stop(), None)

    def test_path_none(self):
        self.fs_poll = uv.FSPoll(self.loop)

        self.assert_raises(uv.error.ArgumentError, self.fs_poll.start)


if __name__ == '__main__':
	unittest.main(verbosity=2)