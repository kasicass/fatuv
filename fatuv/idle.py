from _fatuv import ffi, lib

uv_idle_new             = lib.fatuv_idle_new
uv_idle_delete          = lib.fatuv_idle_delete
uv_idle_init            = lib.fatuv_idle_init
uv_idle_start           = lib.fatuv_idle_start
uv_idle_stop            = lib.fatuv_idle_stop

__all__ = ['Idle',]

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

		self.handle   = None
		self.callback = None
		Idle.instances[handle] = None

		uv_idle_stop(handle)
		uv_idle_delete(handle)

	def _call_callback(self):
		if self.callback:
			self.callback(self)

