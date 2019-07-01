from _fatuv import ffi, lib
from ..handle import Handle
from .. import error

uv_get_pyobj       = lib.fatuv_get_pyobj
uv_set_pyobj       = lib.fatuv_set_pyobj

uv_signal_new      = lib.fatuv_signal_new
uv_signal_delete   = lib.fatuv_signal_delete
uv_signal_init     = lib.fatuv_signal_init
uv_signal_start    = lib.fatuv_signal_start
#uv_signal_start_oneshot = lib.fatuv_signal_start_oneshot
uv_signal_stop     = lib.fatuv_signal_stop

__all__ = ['Signal']

@ffi.def_extern()
def fatuv_signal_callback(signal_handle, signum):
	ptr = uv_get_pyobj(signal_handle)
	obj = ffi.from_handle(ptr)
	obj._call_signal_callback(signum)

class Signal(Handle):
	def __init__(self, loop):
		super(Signal, self).__init__(loop)

		handle = uv_signal_new()
		uv_signal_init(loop.handle, handle)

		self._userdata = ffi.new_handle(self)
		uv_set_pyobj(handle, self._userdata)

		self.handle          = handle
		self.signal_callback = None

	def _dispose(self):
		handle = self.handle
		assert handle

		self.signal_callback = None
		self.handle = None
		
		uv_set_pyobj(handle, ffi.NULL)
		uv_signal_delete(handle)

	def start(self, callback, signum):
		handle = self.handle
		assert handle

		if self.closing:
			raise error.HandleClosedError()

		self.signal_callback = callback
		uv_signal_start(handle, lib.fatuv_signal_callback, signum)

	def _call_signal_callback(self, signum):
		if self.signal_callback:
			self.signal_callback(self, signum)

	"""
	def start_oneshot(self, callback, signum):
		handle = self.handle
		assert handle

		self.callback = callback
		uv_signal_start_oneshot(handle, lib.fatuv_signal_callback, signum)
	"""

	def stop(self):
		handle = self.handle
		assert handle

		if self.closing:
			return

		uv_signal_stop(handle)

		self.signal_callback = None