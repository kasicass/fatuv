from _fatuv import ffi, lib
from .handle import Handle

uv_idle_new             = lib.fatuv_idle_new
uv_idle_delete          = lib.fatuv_idle_delete
uv_idle_init            = lib.fatuv_idle_init
uv_idle_start           = lib.fatuv_idle_start
uv_idle_stop            = lib.fatuv_idle_stop

__all__ = ['Idle',]

@ffi.def_extern()
def fatuv_idle_callback(idle_handle):
	idle = Idle.idle_instances[idle_handle]
	idle._call_idle_callback()

class Idle(Handle):
	idle_instances = {}

	def __init__(self, loop):
		super(Idle, self).__init__(loop)

		handle = uv_idle_new()
		uv_idle_init(loop.handle, handle)

		self.handle        = handle
		self.idle_callback = None

	def _dispose(self):
		assert self.handle
		uv_idle_delete(self.handle)
		self.handle = None

	def start(self, callback):
		handle = self.handle
		assert handle

		self.idle_callback          = callback
		Idle.idle_instances[handle] = self
		uv_idle_start(handle, lib.fatuv_idle_callback)  # TODO: check return value

	def _call_idle_callback(self):
		if self.idle_callback:
			self.idle_callback(self)

	def stop(self):
		handle = self.handle
		assert handle

		uv_idle_stop(handle)

		Idle.idle_instances[handle] = None
		self.idle_callback          = None

