import sys
from _fatcore import ffi, lib
from ..handle import Handle
from .. import error

uv_get_pyobj    = lib.fatuv_get_pyobj
uv_set_pyobj    = lib.fatuv_set_pyobj

uv_async_new    = lib.fatuv_async_new
uv_async_init   = lib.fatuv_async_init
uv_async_delete = lib.fatuv_async_delete
uv_async_send   = lib.fatuv_async_send


@ffi.def_extern()
def fatuv_async_callback(async_handle):
	ptr = uv_get_pyobj(async_handle)
	obj = ffi.from_handle(ptr)
	obj._call_async_callback()

class Async(Handle):
	def __init__(self, loop = None, callback = None):
		super(Async, self).__init__(loop)

		handle = uv_async_new()
		uv_async_init(self.loop.handle, handle, lib.fatuv_async_callback)

		self._userdata = ffi.new_handle(self)
		uv_set_pyobj(handle, self._userdata)

		self.handle = handle
		self.async_callback = callback
	
	def _dispose(self):
		handle = self.handle
		assert handle

		self.async_callback = None
		self.handle		 = None
		self._userdata	  = None

		uv_set_pyobj(handle, ffi.NULL)
		uv_async_delete(handle)

	def send(self, callback=None):
		handle = self.handle
		assert handle

		if self.closing:
			raise error.HandleClosedError()

		self.async_callback = callback or self.async_callback
		code = uv_async_send(self.handle)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)
	
	def _call_async_callback(self):
		if self.async_callback:
			self.async_callback(self)

