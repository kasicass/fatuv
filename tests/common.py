# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, division, absolute_import

import contextlib
import os
import os.path
import platform
import sys
sys.path.append('.')
import unittest

import fatuv as uv


__dir__ = os.path.dirname(__file__)

PY2_RERAISE = '''
def reraise(exc_type, exc_value, exc_traceback):
	raise exc_type, exc_value, exc_traceback
'''

if uv.common.is_py2:
	exec(PY2_RERAISE)
else:
	def reraise(_, exc_value, exc_traceback):
		raise exc_value.with_traceback(exc_traceback)

sys_platform = 'linux' if sys.platform.startswith('linux') else sys.platform

class TestLoop(uv.Loop):
	def __init__(self,default=True):
		super(TestLoop, self).__init__(default=default)

	def run(self, mode=uv.UV_RUN_DEFAULT):
		self.exc_type = None
		result = super(TestLoop, self).run(mode)
		if self.exc_type is not None:
			reraise(self.exc_type, self.exc_value, self.exc_traceback)
		return result


class TestCase(unittest.TestCase):
	def setUp(self):
		self.loop = TestLoop(default=False)
		self.set_up()

	def tearDown(self):
		self.tear_down()
		if not self.loop.closed:
			self.loop.close_all_handles(uv.common.dummy_callback)
			self.loop.run()
			self.loop.close()

	def set_up(self):
		pass

	def tear_down(self):
		pass

	@contextlib.contextmanager
	def should_raise(self, expected):
		try:
			yield
		except Exception as exception:
			if not isinstance(exception, expected):
				import sys
				exc_type, exc_value, exc_traceback = sys.exc_info()
				reraise(exc_type, exc_value, exc_traceback)
		else:
			msg = 'exception %s should have been raised' % str(expected)
			self.assert_false(True, msg=msg)

	assert_true = unittest.TestCase.assertTrue
	assert_false = unittest.TestCase.assertFalse

	assert_raises = unittest.TestCase.assertRaises

	assert_equal = unittest.TestCase.assertEqual
	assert_not_equal = unittest.TestCase.assertNotEqual
	assert_greater = unittest.TestCase.assertGreater
	assert_greater_equal = unittest.TestCase.assertGreaterEqual
	assert_less = unittest.TestCase.assertLess
	assert_less_equal = unittest.TestCase.assertLessEqual

	assert_in = unittest.TestCase.assertIn

	assert_is = unittest.TestCase.assertIs
	assert_is_not = unittest.TestCase.assertIsNot
	assert_is_instance = unittest.TestCase.assertIsInstance
	assert_is_none = unittest.TestCase.assertIsNone
	assert_is_not_none = unittest.TestCase.assertIsNotNone

