from _fatuv import ffi, lib

uv_default_loop = lib.fatuv_default_loop

uv_loop_new    = lib.fatuv_loop_new
uv_loop_delete = lib.fatuv_loop_delete
uv_loop_init   = lib.fatuv_loop_init
uv_loop_close  = lib.fatuv_loop_close

uv_run = lib.fatuv_run

uv_idle_new    = lib.fatuv_idle_new
uv_idle_delete = lib.fatuv_idle_delete
uv_idle_init   = lib.fatuv_idle_init
uv_idle_start  = lib.fatuv_idle_start
uv_idle_stop   = lib.fatuv_idle_stop

__all__ = [
	'UV_RUN_DEFAULT', 'UV_RUN_ONCE', 'UV_RUN_NOWAIT',
	'Loop', 'Idle'
]

UV_RUN_DEFAULT = lib.FATUV_RUN_DEFAULT
UV_RUN_ONCE    = lib.FATUV_RUN_ONCE
UV_RUN_NOWAIT  = lib.FATUV_RUN_NOWAIT

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

