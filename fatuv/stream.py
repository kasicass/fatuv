from _fatuv import ffi, lib
from .handle import Handle
from .error import StreamError
from .internal import get_strerror

uv_get_pyobj  = lib.fatuv_get_pyobj
uv_set_pyobj  = lib.fatuv_set_pyobj

uv_listen     = lib.fatuv_listen
uv_accept     = lib.fatuv_accept
uv_read_start = lib.fatuv_read_start
uv_read_stop  = lib.fatuv_read_stop

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
		obj._call_read_callback(data, nread)
	else:
		obj._call_read_callback(None, nread)

class Stream(Handle):
	def _dispose(self):
		handle = self.handle
		assert handle

	def listen(self, callback, backlog=128):
		handle = self.handle
		assert self.handle

		self.conn_callback = callback
		return uv_listen(handle, backlog, lib.fatuv_connection_callback)

	def _call_conn_callback(self, status):
		callback = self.conn_callback
		if callback:
			callback(self, status)

	def accept(self, client):
		if not isinstance(client, Stream):
			raise TypeError("Only stream objects are supported for accept")

		assert self.handle
		err = uv_accept(self.handle, client.handle)
		if err < 0:
			raise StreamError((err, get_strerror))

	def start_read(self, callback):
		handle = self.handle
		assert self.handle

		self.read_callback = callback
		return uv_read_start(handle, lib.fatuv_read_callback)

	def _call_read_callback(self, data, error):
		callback = self.read_callback
		if callback:
			callback(self, data, error)

