import sys
sys.path.append('.')

from fatuv.internal import get_strerror, get_err_name

print get_err_name(-9)
print get_strerror(-9)

