import time
from fatuv import Loop
from fatuv import Timer

counter = 0

def repeat_callback(handle):
	global counter
	counter += 1	
	if counter < 20:
		print 'repeat counter = %d, %s' % (counter, time.strftime('%H:%M:%S'))
	else:
		handle.stop()

def timer_callback(handle):
	global counter
	counter += 1
	if counter < 10:
		print 'counter = %d, %s' % (counter, time.strftime('%H:%M:%S'))
	else:
		handle.callback = repeat_callback
		handle.repeat   = 3.5 # 3.5s
		handle.again()

loop = Loop.default_loop()

handle = Timer(loop)
handle.start(timer_callback, 1.5, 0.5) # timeout = 1.5s, repeat = 0.5s

print 'timer start,', time.strftime('%H:%M:%S')
print 'timer repeat =', handle.repeat
loop.run()

