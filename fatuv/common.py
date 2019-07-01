# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import platform
import sys
from collections import OrderedDict

is_py2 = sys.version_info[0] == 2
is_py3 = sys.version_info[0] == 3

is_pypy = platform.python_implementation().lower() == 'pypy'
is_cpython = platform.python_implementation().lower() == 'cpython'

is_posix = os.name == 'posix'
is_nt = os.name == 'nt'
is_linux = sys.platform.startswith('linux')
is_win32 = sys.platform == 'win32'


def dummy_callback(*arguments, **keywords): pass
