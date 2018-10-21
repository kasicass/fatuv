import sys
sys.path.append('.')

from fatuv import Loop
from fatuv import Idle

counter = 0 
def idle_callback(myidle):
	global counter
	counter += 1
	if counter >= 1000000:
		myidle.close()

loop = Loop.default_loop()

myidle = Idle(loop)
myidle.start(idle_callback)

print 'Idling...'
loop.run()

print 'counter =', counter

