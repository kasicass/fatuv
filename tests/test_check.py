# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from common import TestCase
import unittest
import fatuv as uv

class TestCheck(TestCase):
    def test_check(self):
        def on_check(check):
            self.on_check_called += 1
            if self.on_check_called > 5:
                check.close()

        def on_timeout(timer):
            self.on_timeout_called += 1
            if self.on_timeout_called > 5:
                timer.close()

        self.on_check_called = 0
        self.on_timeout_called = 0

        self.check = uv.Check(self.loop)
        self.check.start(on_check)

        self.timer = uv.Timer(self.loop)
        self.timer.start(on_timeout, 1, 1)

        self.loop.run()

        self.assert_less_equal(self.on_timeout_called, self.on_check_called)

    def test_check_stop(self):
        self.check = uv.Check(self.loop)
        self.check.start()
        self.check.stop()
        self.loop.run()

    def test_closed(self):
        self.check = uv.Check(self.loop)
        self.check.close()

        self.assert_raises(uv.HandleClosedError, self.check.start)
        self.assert_is(self.check.stop(), None)

if __name__ == '__main__':
	unittest.main(verbosity=2)