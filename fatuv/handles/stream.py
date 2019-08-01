from _fatuv import ffi, lib
from ..handle import Handle
from .. import error
from ..error import StreamError
from ..internal import get_strerror

uv_get_pyobj    = lib.fatuv_get_pyobj
uv_set_pyobj    = lib.fatuv_set_pyobj

uv_listen       = lib.fatuv_listen
uv_accept       = lib.fatuv_accept
uv_read_start   = lib.fatuv_read_start
uv_read_stop    = lib.fatuv_read_stop
uv_write        = lib.fatuv_write
uv_try_write    = lib.fatuv_try_write
uv_shutdown     = lib.fatuv_shutdown
uv_is_readable  = lib.fatuv_is_readable
uv_is_writable  = lib.fatuv_is_writable

__all__ = ['Stream']

@ffi.def_extern()
def fatuv_connection_callback(stream_handle, status):
	ptr = uv_get_pyobj(stream_handle)
	obj = ffi.from_handle(ptr)
	obj._call_conn_callback(status)

@ffi.def_extern()
def fatuv_read_callback(stream_handle, nread, buf):
	ptr = uv_get_pyobj(stream_handle)
	obj = ffi.from_handle(ptr)

	if nread < 0:
		obj._call_read_callback(None, nread)
	elif nread > 0:
		data = ffi.unpack(buf.base, nread)
		obj._call_read_callback(data, 0)
	else:
		obj._call_read_callback(None, nread)

@ffi.def_extern()
def fatuv_write_callback(stream_handle, status):
	ptr = uv_get_pyobj(stream_handle)
	obj = ffi.from_handle(ptr)
	obj._call_write_callback(status)

@ffi.def_extern()
def fatuv_shutdown_callback(stream_handle, status):
	ptr = uv_get_pyobj(stream_handle)
	obj = ffi.from_handle(ptr)
	obj._call_shutdown_callback(status)

class Stream(Handle):
	def _dispose(self):
		handle = self.handle
		assert handle

	def listen(self, callback, backlog=128):
		handle = self.handle
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		self.conn_callback = callback
		err = uv_listen(handle, backlog, lib.fatuv_connection_callback)
		if err != error.STATUS_SUCCESS:
			raise StreamError((err,get_strerror(err)))

	def _call_conn_callback(self, status):
		callback = self.conn_callback
		if callback:
			callback(self, status)

	def accept(self, client):
		if self.closing:
			raise error.HandleClosedError()
		if not isinstance(client, Stream):
			raise TypeError("Only stream objects are supported for accept")
		assert self.handle
		err = uv_accept(self.handle, client.handle)
		if err < 0:
			raise StreamError((err,get_strerror(err)))

	def start_read(self, callback):
		handle = self.handle
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		self.read_callback = callback
		code = uv_read_start(handle, lib.fatuv_read_callback)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def _call_read_callback(self, data, error):
		callback = self.read_callback
		if callback:
			callback(self, data, error)
	
	def stop_read(self):
		if self.closing:
			return
		handle = self.handle
		assert self.handle
		code = uv_read_stop(handle)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def write(self, data, callback=None):
		handle = self.handle
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		self.write_callback = callback
		uv_write(handle, data, len(data), lib.fatuv_write_callback)

	def _call_write_callback(self, status):
		callback = self.write_callback
		if callback:
			callback(self, status)

	def try_write(self, data):
		handle = self.handle
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		code = uv_try_write(handle, data, len(data))
		if code < 0:
			raise error.UVError(code)
		return code

	def shutdown(self, callback=None):
		handle = self.handle
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		self.shutdown_callback = callback
		uv_shutdown(handle,lib.fatuv_shutdown_callback)

	def _call_shutdown_callback(self, status):
		callback = self.shutdown_callback
		if callback:
			callback(self,status)

	@property
	def readable(self):
		if self.closing:
			return False
		return bool(uv_is_readable(self.handle))

	@property
	def writable(self):
		if self.closing:
			return False
		return bool(uv_is_writable(self.handle))
