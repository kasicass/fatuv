import sys
sys.path.append('.')

import fatuv
from fatuv.error import HandleError

loop = fatuv.Loop.default_loop()
idle = fatuv.Idle(loop)
try:
	print idle.fileno()
except HandleError:
	print 'right!'

tcp = fatuv.TCP(loop)
tcp.bind(('0.0.0.0', 25000))
print tcp.fileno()

tcp2 = fatuv.TCP(loop)
tcp2.bind(('0.0.0.0', 25001))
print tcp2.fileno()

