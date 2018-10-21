from _fatuv import ffi, lib
from .handle import Handle

uv_signal_new           = lib.fatuv_signal_new
uv_signal_delete        = lib.fatuv_signal_delete
uv_signal_init          = lib.fatuv_signal_init
uv_signal_start         = lib.fatuv_signal_start
#uv_signal_start_oneshot = lib.fatuv_signal_start_oneshot
uv_signal_stop          = lib.fatuv_signal_stop

__all__ = ['Signal']

@ffi.def_extern()
def fatuv_signal_callback(signal_handle, signum):
	signal = Signal.signal_instances[signal_handle]
	signal._call_signal_callback(signum)

class Signal(Handle):
	signal_instances = {}

	def __init__(self, loop):
		super(Signal, self).__init__(loop)

		handle = uv_signal_new()
		uv_signal_init(loop.handle, handle)

		self.handle          = handle
		self.signal_callback = None

	def _dispose(self):
		handle = self.handle
		assert handle

		Signal.signal_instances.pop(handle, None)
		self.signal_callback = None
		
		uv_signal_delete(handle)
		self.handle = None

	def start(self, callback, signum):
		handle = self.handle
		assert handle

		self.signal_callback            = callback
		Signal.signal_instances[handle] = self
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

		uv_signal_stop(handle)

		Signal.signal_instances[handle] = None
		self.signal_callback            = None

