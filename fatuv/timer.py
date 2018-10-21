from _fatuv import ffi, lib

uv_timer_new            = lib.fatuv_timer_new
uv_timer_delete         = lib.fatuv_timer_delete
uv_timer_init           = lib.fatuv_timer_init
uv_timer_start          = lib.fatuv_timer_start
uv_timer_stop           = lib.fatuv_timer_stop
uv_timer_again          = lib.fatuv_timer_again
uv_timer_set_repeat     = lib.fatuv_timer_set_repeat
uv_timer_get_repeat     = lib.fatuv_timer_get_repeat

__all__ = ['Timer']

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

		self.handle   = None
		self.callback = None
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

