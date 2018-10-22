from _fatuv import ffi, lib
from .stream import Stream
from .error import TCPError
from .internal import get_strerror

uv_send_buffer_size = lib.fatuv_send_buffer_size
uv_recv_buffer_size = lib.fatuv_recv_buffer_size

uv_tcp_new            = lib.fatuv_tcp_new
uv_tcp_delete         = lib.fatuv_tcp_delete
uv_tcp_init           = lib.fatuv_tcp_init
uv_tcp_nodelay        = lib.fatuv_tcp_nodelay
uv_tcp_keepalive      = lib.fatuv_tcp_keepalive
uv_tcp_v4_bind        = lib.fatuv_tcp_v4_bind
uv_tcp_v4_getpeername = lib.fatuv_tcp_v4_getpeername

__all__ = ['TCP']

class TCP(Stream):
	def __init__(self, loop):
		super(TCP, self).__init__(loop)

		handle = uv_tcp_new();
		uv_tcp_init(loop.handle, handle)

		self.handle = handle

	def _dispose(self):
		super(TCP, self)._dispose()

		handle = self.handle
		assert self.handle

		uv_tcp_delete(handle)

	def bind(self, addr):
		assert self.handle
		ip, port = addr
		ip = ffi.new('char[]', ip)
		return uv_tcp_v4_bind(self.handle, ip, port)

	def getpeername(self):
		assert self.handle
		ip   = ffi.new('char[16]')
		port = ffi.new('int*')

		err = uv_tcp_v4_getpeername(self.handle, ip, port)
		if err < 0:
			raise TCPError((err, get_strerror(err)))

		return ffi.string(ip), port[0]

	def nodelay(self, enable):
		assert self.handle
		return uv_tcp_nodelay(self.handle, 1 if enable else 0)

	def keepalive(self, enable, delay):
		assert self.handle
		return uv_tcp_keepalive(self.handle, 1 if enable else 0, delay)

	@property
	def send_buffer_size(self):
		assert self.handle
		ptr = ffi.new('int*')
		ptr[0] = 0

		err = uv_send_buffer_size(self.handle, ptr)
		if err < 0:
			raise TCPError((err, get_strerror(err)))

		return ptr[0]

	@send_buffer_size.setter
	def send_buffer_size(self, value):
		assert self.handle
		ptr = ffi.new('int*')
		ptr[0] = value

		err = uv_send_buffer_size(self.handle, ptr)
		if err < 0:
			raise TCPError((err, get_strerror(err)))

		return ptr[0]

	@property
	def receive_buffer_size(self):
		assert self.handle
		ptr = ffi.new('int*')
		ptr[0] = 0

		err = uv_recv_buffer_size(self.handle, ptr)
		if err < 0:
			raise TCPError((err, get_strerror(err)))

		return ptr[0]

	@receive_buffer_size.setter
	def receive_buffer_size(self, value):
		assert self.handle
		ptr = ffi.new('int*')
		ptr[0] = value

		err = uv_recv_buffer_size(self.handle, ptr)
		if err < 0:
			raise TCPError((err, get_strerror(err)))

		return ptr[0]

