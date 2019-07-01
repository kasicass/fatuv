# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from common import TestCase
import unittest
import os
import signal
import threading
import fatuv as uv

class TestSignal(TestCase):
    def test_signal(self):
        self.signum = None

        def on_signal(signal_handle, signum):
            self.signum = signum
            signal_handle.stop()

        self.signal = uv.Signal(self.loop)
        self.signal.start(on_signal, signal.SIGUSR1)

        thread = threading.Thread(target=self.loop.run)
        thread.start()

        os.kill(os.getpid(), signal.SIGUSR1)

        thread.join()

        self.assert_equal(self.signum, signal.SIGUSR1)

    def test_closed(self):
        self.signal = uv.Signal(self.loop)
        self.signal.close()

        self.assert_raises(uv.HandleClosedError, self.signal.start, None, 2)
        self.assert_is(self.signal.stop(), None)

if __name__ == '__main__':
	unittest.main(verbosity=2)