from _fatuv import ffi, lib

uv_signal_new           = lib.fatuv_signal_new
uv_signal_delete        = lib.fatuv_signal_delete
uv_signal_init          = lib.fatuv_signal_init
uv_signal_start         = lib.fatuv_signal_start
#uv_signal_start_oneshot = lib.fatuv_signal_start_oneshot
uv_signal_stop          = lib.fatuv_signal_stop

__all__ = ['Signal']

@ffi.def_extern()
def fatuv_signal_callback(signal_handle, signum):
	signal = Signal.instances[signal_handle]
	signal._call_callback(signum)

class Signal(object):
	instances = {}

	def __init__(self, loop):
		handle = uv_signal_new()
		uv_signal_init(loop.handle, handle)
		Signal.instances[handle] = self

		self.handle   = handle
		self.callback = None

	def start(self, callback, signum):
		handle = self.handle
		assert handle

		self.callback = callback
		uv_signal_start(handle, lib.fatuv_signal_callback, signum)

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

		self.handle   = None
		self.callback = None
		Signal.instances[handle] = None

		uv_signal_stop(handle)
		# uv_signal_delete(handle)  # or libuv will crash (uv-timer.py)

	def _call_callback(self, signum):
		if self.callback:
			self.callback(self, signum)

