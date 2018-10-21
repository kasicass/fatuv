from _fatuv import ffi, lib

uv_default_loop     = lib.fatuv_default_loop

uv_loop_new         = lib.fatuv_loop_new
uv_loop_delete      = lib.fatuv_loop_delete
uv_loop_init        = lib.fatuv_loop_init
uv_loop_close       = lib.fatuv_loop_close

uv_run              = lib.fatuv_run

uv_idle_new         = lib.fatuv_idle_new
uv_idle_delete      = lib.fatuv_idle_delete
uv_idle_init        = lib.fatuv_idle_init
uv_idle_start       = lib.fatuv_idle_start
uv_idle_stop        = lib.fatuv_idle_stop

uv_timer_new        = lib.fatuv_timer_new
uv_timer_delete     = lib.fatuv_timer_delete
uv_timer_init       = lib.fatuv_timer_init
uv_timer_start      = lib.fatuv_timer_start
uv_timer_stop       = lib.fatuv_timer_stop
uv_timer_again      = lib.fatuv_timer_again
uv_timer_set_repeat = lib.fatuv_timer_set_repeat
uv_timer_get_repeat = lib.fatuv_timer_get_repeat

__all__ = [
	'UV_RUN_DEFAULT', 'UV_RUN_ONCE', 'UV_RUN_NOWAIT',
	'Loop', 'Idle'
]

UV_RUN_DEFAULT = lib.FATUV_RUN_DEFAULT
UV_RUN_ONCE    = lib.FATUV_RUN_ONCE
UV_RUN_NOWAIT  = lib.FATUV_RUN_NOWAIT

#
# Loop
#

class Loop(object):
	@staticmethod
	def default_loop():
		return Loop(uv_default_loop())

	def __init__(self, handle=None):
		self.handle = handle or uv_loop_new()
		uv_loop_init(self.handle)

	def run(self, mode=UV_RUN_DEFAULT):
		assert self.handle
		uv_run(self.handle, mode)

	def close(self):
		assert self.handle
		uv_loop_close(self.handle)
		uv_loop_delete(self.handle)
		self.handle = None

#
# Idle
#

@ffi.def_extern()
def fatuv_idle_callback(idle_handle):
	idle = Idle.instances[idle_handle]
	idle._call_callback()

class Idle(object):
	instances = {}

	def __init__(self, loop):
		handle = uv_idle_new()
		uv_idle_init(loop.handle, handle)
		Idle.instances[handle] = self

		self.handle   = handle
		self.callback = None

	def start(self, callback):
		handle = self.handle
		assert handle

		self.callback = callback
		uv_idle_start(handle, lib.fatuv_idle_callback)

	def stop(self):
		handle = self.handle
		assert handle

		self.handle = None
		Idle.instances[handle] = None

		uv_idle_stop(handle)
		uv_idle_delete(handle)

	def _call_callback(self):
		if self.callback:
			self.callback(self)

#
# Timer
#

@ffi.def_extern()
def fatuv_timer_callback(timer_handle):
	timer = Timer.instances[timer_handle]
	timer._call_callback()

class Timer(object):
	instances = {}

	def __init__(self, loop):
		handle = uv_timer_new()
		uv_timer_init(loop.handle, handle)
		Timer.instances[handle] = self

		self.handle   = handle
		self.callback = None

	def start(self, callback, timeout, repeat):
		handle = self.handle
		assert handle

		self.callback = callback
		uv_timer_start(handle, lib.fatuv_timer_callback, int(timeout*1000), int(repeat*1000))

	def stop(self):
		handle = self.handle
		assert handle

		self.handle = None
		Timer.instances[handle] = None

		uv_timer_stop(handle)
		uv_timer_delete(handle)

	def again(self):
		assert self.handle
		uv_timer_again(self.handle)
	
	@property
	def repeat(self):
		assert self.handle
		return float(uv_timer_get_repeat(self.handle)) / 1000

	@repeat.setter
	def repeat(self, value):
		assert self.handle
		uv_timer_set_repeat(self.handle, int(value*1000))

	def _call_callback(self):
		if self.callback:
			self.callback(self)

