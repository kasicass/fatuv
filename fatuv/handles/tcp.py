from _fatuv import ffi, lib
from .stream import Stream
from ..error import TCPError
from ..internal import get_strerror
from .. import error

uv_get_pyobj          = lib.fatuv_get_pyobj
uv_set_pyobj          = lib.fatuv_set_pyobj
uv_send_buffer_size   = lib.fatuv_send_buffer_size
uv_recv_buffer_size   = lib.fatuv_recv_buffer_size

uv_tcp_new            = lib.fatuv_tcp_new
uv_tcp_delete         = lib.fatuv_tcp_delete
uv_tcp_init           = lib.fatuv_tcp_init
uv_tcp_nodelay        = lib.fatuv_tcp_nodelay
uv_tcp_keepalive      = lib.fatuv_tcp_keepalive
uv_tcp_v4_bind        = lib.fatuv_tcp_v4_bind
uv_tcp_v4_getpeername = lib.fatuv_tcp_v4_getpeername
uv_tcp_open           = lib.fatuv_tcp_open
uv_tcp_connect        = lib.fatuv_tcp_connect
uv_tcp_simultaneous_accepts = lib.fatuv_tcp_simultaneous_accepts

__all__ = ['TCP']

@ffi.def_extern()
def fatuv_tcp_connect_cb(handle, status):
	ptr = uv_get_pyobj(handle)
	obj = ffi.from_handle(ptr)
	obj._call_tcp_connect_callback(status)

class TCP(Stream):
	def __init__(self, loop):
		super(TCP, self).__init__(loop)

		handle = uv_tcp_new();
		uv_tcp_init(loop.handle, handle)

		self._userdata = ffi.new_handle(self)
		uv_set_pyobj(handle, self._userdata)
		self.tcp_connect_callback = None
		self.handle = handle

	def _dispose(self):
		handle = self.handle
		assert self.handle

		self.tcp_connect_callback = None
		self.handle    = None
		self._userdata = None
		
		uv_set_pyobj(handle, ffi.NULL)
		uv_tcp_delete(handle)

	def open(self, fd):
		if self.closing:
			raise error.HandleClosedError()
		code = uv_tcp_open(self.handle, fd)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def bind(self, addr):
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		ip, port = addr
		ip = ffi.new('char[]', ip)
		code = uv_tcp_v4_bind(self.handle, ip, port)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def getpeername(self):
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		ip   = ffi.new('char[16]')
		port = ffi.new('int*')

		err = uv_tcp_v4_getpeername(self.handle, ip, port)
		if err < 0:
			raise TCPError((err, get_strerror(err)))

		return ffi.string(ip), port[0]

	def nodelay(self, enable):
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		return uv_tcp_nodelay(self.handle, 1 if enable else 0)

	def keepalive(self, enable, delay):
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		return uv_tcp_keepalive(self.handle, 1 if enable else 0, delay)

	def connect(self, ip, port, callback=None):
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		self.tcp_connect_callback = callback or self.tcp_connect_callback
		uv_tcp_connect(self.handle, ip, port, lib.fatuv_tcp_connect_cb)

	def _call_tcp_connect_callback(self,status):
		callback = self.tcp_connect_callback
		if callback:
			callback(self,status)

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

	def set_simultaneous_accepts(self,enable):
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		return uv_tcp_simultaneous_accepts(self.handle, enable)