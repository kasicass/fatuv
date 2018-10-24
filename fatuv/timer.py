from _fatuv import ffi, lib
from .handle import Handle

uv_timer_new            = lib.fatuv_timer_new
uv_timer_delete         = lib.fatuv_timer_delete
uv_timer_set_pyobj      = lib.fatuv_timer_set_pyobj
uv_timer_get_pyobj      = lib.fatuv_timer_get_pyobj
uv_timer_init           = lib.fatuv_timer_init
uv_timer_start          = lib.fatuv_timer_start
uv_timer_stop           = lib.fatuv_timer_stop
uv_timer_again          = lib.fatuv_timer_again
uv_timer_set_repeat     = lib.fatuv_timer_set_repeat
uv_timer_get_repeat     = lib.fatuv_timer_get_repeat

__all__ = ['Timer']

@ffi.def_extern()
def fatuv_timer_callback(timer_handle):
	ptr = uv_timer_get_pyobj(timer_handle)
	obj = ffi.from_handle(ptr)
	obj._call_timer_callback()

class Timer(Handle):
	def __init__(self, loop):
		super(Timer, self).__init__(loop)

		handle = uv_timer_new()
		uv_timer_init(loop.handle, handle)

		self._userdata = ffi.new_handle(self)
		uv_timer_set_pyobj(handle, self._userdata)

		self.handle         = handle
		self.timer_callback = None

	def _dispose(self):
		handle = self.handle
		assert handle

		self.timer_callback = None
		self.handle         = None
		self._userdata      = None

		uv_timer_set_pyobj(handle, ffi.NULL)
		uv_timer_delete(handle)

	def start(self, callback, timeout, repeat):
		handle = self.handle
		assert handle

		self.timer_callback = callback
		uv_timer_start(handle, lib.fatuv_timer_callback, int(timeout*1000), int(repeat*1000))

	def _call_timer_callback(self):
		if self.timer_callback:
			self.timer_callback(self)

	def stop(self):
		handle = self.handle
		assert handle

		uv_timer_stop(handle)
		self.timer_callback = None

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

