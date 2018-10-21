from _fatuv import ffi, lib

uv_send_buffer_size = lib.fatuv_send_buffer_size
uv_recv_buffer_size = lib.fatuv_recv_buffer_size

uv_tcp_new          = lib.fatuv_tcp_new
uv_tcp_delete       = lib.fatuv_tcp_delete
uv_tcp_init         = lib.fatuv_tcp_init
uv_tcp_nodelay      = lib.fatuv_tcp_nodelay
uv_tcp_keepalive    = lib.fatuv_tcp_keepalive

__all__ = ['TCP',]

class TCP(object):
	def __init__(self, loop):
		handle = uv_tcp_new();
		uv_tcp_init(loop.handle, handle)

		self.handle = handle

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
		errno = uv_send_buffer_size(self.handle, ptr)
		if errno == 0:
			return ptr[0]
		else:
			# TODO(kasicass): define a new error type?
			raise SystemError('get_send_buffer_size: '+str(errno))

	@send_buffer_size.setter
	def send_buffer_size(self, value):
		assert self.handle
		ptr = ffi.new('int*')
		ptr[0] = value
		errno = uv_send_buffer_size(self.handle, ptr)
		if errno == 0:
			return ptr[0]
		else:
			raise SystemError('set_send_buffer_size: '+str(errno))

	@property
	def receive_buffer_size(self):
		assert self.handle
		ptr = ffi.new('int*')
		ptr[0] = 0
		errno = uv_recv_buffer_size(self.handle, ptr)
		if errno == 0:
			return ptr[0]
		else:
			raise SystemError('get_recv_buffer_size: '+str(errno))

	@receive_buffer_size.setter
	def receive_buffer_size(self, value):
		assert self.handle
		ptr = ffi.new('int*')
		ptr[0] = value
		errno = uv_recv_buffer_size(self.handle, ptr)
		if errno == 0:
			return ptr[0]
		else:
			raise SystemError('set_recv_buffer_size: '+str(errno))

