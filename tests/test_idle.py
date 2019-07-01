# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from common import TestCase
import unittest
import fatuv as uv

class TestIdle(TestCase):
    def test_idle(self):
        def on_idle(idle):
            self.on_idle_called += 1
            if self.on_idle_called > 5:
                idle.stop()

        self.on_idle_called = 0

        self.idle = uv.Idle(self.loop)
        self.idle.start(on_idle)

        self.loop.run()

        self.assert_equal(self.on_idle_called, 6)

    def test_closed(self):
        self.idle = uv.Idle(self.loop)
        self.idle.close()

        self.assert_raises(uv.HandleClosedError, self.idle.start, None)
        self.assert_is(self.idle.stop(), None)

if __name__ == '__main__':
	unittest.main(verbosity=2)