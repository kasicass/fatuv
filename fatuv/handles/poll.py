import sys
from _fatcore import ffi, lib
from ..handle import Handle
from .. import error

uv_get_pyobj    = lib.fatuv_get_pyobj
uv_set_pyobj    = lib.fatuv_set_pyobj

uv_poll_new     = lib.fatuv_poll_new
uv_poll_delete  = lib.fatuv_poll_delete
uv_poll_init    = lib.fatuv_poll_init
uv_poll_start   = lib.fatuv_poll_start
uv_poll_stop    = lib.fatuv_poll_stop

__all__ = ['Poll']

@ffi.def_extern()
def fatuv_poll_callback(poll_handle, status, events):
	ptr = uv_get_pyobj(poll_handle)
	obj = ffi.from_handle(ptr)
	obj._call_poll_callback(status, events)

class Poll(Handle):
	def __init__(self, loop, fd, callback=None):
		super(Poll, self).__init__(loop)

		handle = uv_poll_new()
		uv_poll_init(loop.handle, handle, fd)

		self.fd = fd

		self._userdata = ffi.new_handle(self)
		uv_set_pyobj(handle, self._userdata)

		self.handle = handle
		self.poll_callback = callback

	def _dispose(self):
		handle = self.handle
		assert handle

		self.poll_callback = None
		self.handle         = None
		self._userdata      = None

		uv_set_pyobj(handle, ffi.NULL)
		uv_poll_delete(handle)

	def fileno(self):
		return self.fd

	def start(self, events=lib.FATUV_POLL_EVENT_READABLE, callback=None):
		handle = self.handle
		assert handle

		if self.closing:
			raise error.HandleClosedError()

		self.poll_callback = callback or self.poll_callback
		code = uv_poll_start(self.handle, events, lib.fatuv_poll_callback)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def _call_poll_callback(self, status, events):
		if self.poll_callback:
			self.poll_callback(self, status, events)

	def stop(self):
		handle = self.handle
		assert handle

		if self.closing:
			return

		code = uv_poll_stop(handle)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)
		self.poll_callback = None
