from _fatuv import ffi, lib

uv_default_loop = lib.fatuv_default_loop

uv_get_pyobj    = lib.fatuv_get_pyobj
uv_set_pyobj    = lib.fatuv_set_pyobj

uv_loop_new     = lib.fatuv_loop_new
uv_loop_delete  = lib.fatuv_loop_delete
uv_loop_init    = lib.fatuv_loop_init
uv_loop_close   = lib.fatuv_loop_close
uv_walk         = lib.fatuv_walk
uv_stop         = lib.fatuv_stop

uv_run          = lib.fatuv_run

__all__ = [
	'UV_RUN_DEFAULT', 'UV_RUN_ONCE', 'UV_RUN_NOWAIT',
	'Loop',
]

UV_RUN_DEFAULT  = lib.FATUV_RUN_DEFAULT
UV_RUN_ONCE     = lib.FATUV_RUN_ONCE
UV_RUN_NOWAIT   = lib.FATUV_RUN_NOWAIT

@ffi.def_extern()
def fatuv_walk_callback(uv_handle, c_handles_set):
	ptr = uv_get_pyobj(uv_handle)
	handle = ffi.from_handle(ptr)
	if handle is not None:
		ffi.from_handle(c_handles_set).add(handle)

class Loop(object):
	@staticmethod
	def default_loop():
		return Loop(uv_default_loop())

	def __init__(self, default=True):
		self.handle = uv_default_loop() if default else uv_loop_new()
		uv_loop_init(self.handle)
		self.pending = set()

	def run(self, mode=UV_RUN_DEFAULT):
		assert self.handle
		uv_run(self.handle, mode)

	def close(self):
		assert self.handle
		uv_loop_close(self.handle)
		uv_loop_delete(self.handle)
		self.handle = None

	def stop(self):
		if self.closed:
			return
		uv_stop(self.handle)

	@property
	def closed(self):
		assert self.handle
		return bool(lib.fatuv_is_closing(self.handle))

	@property
	def handles(self):
		handles = set()
		if not self.closed:
			uv_walk(self.handle, lib.fatuv_walk_callback, ffi.new_handle(handles))
		return handles
	
	def close_all_handles(self, on_closed=None):
		for handle in self.handles:
			handle.close(on_closed)

