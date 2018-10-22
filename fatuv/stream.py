from _fatuv import ffi, lib
from .handle import Handle
from .error import StreamError
from .internal import get_strerror

uv_listen = lib.fatuv_listen
uv_accept = lib.fatuv_accept

__all__ = ['Stream']

@ffi.def_extern()
def fatuv_connection_callback(stream_handle, status):
	obj = Stream.conn_instances[stream_handle]
	obj._call_conn_callback(status)

class Stream(Handle):
	conn_instances = {}

	def __init__(self, loop):
		super(Stream, self).__init__(loop)
		self.conn_callback = None

	def _dispose(self):
		handle = self.handle
		assert handle

		Stream.conn_instances.pop(handle, None)

	def listen(self, callback, backlog=128):
		handle = self.handle
		assert self.handle

		self.conn_callback            = callback
		Stream.conn_instances[handle] = self
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

