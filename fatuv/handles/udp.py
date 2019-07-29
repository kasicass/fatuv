from _fatuv import ffi, lib
from ..handle import Handle
from ..internal import get_strerror
from .. import error

uv_get_pyobj          = lib.fatuv_get_pyobj
uv_set_pyobj          = lib.fatuv_set_pyobj

uv_udp_new            = lib.fatuv_udp_new
uv_udp_delete         = lib.fatuv_udp_delete
uv_udp_init           = lib.fatuv_udp_init
uv_udp_open			  = lib.fatuv_udp_open
uv_udp_v4_bind		  = lib.fatuv_udp_v4_bind
uv_udp_send			  = lib.fatuv_udp_send
uv_udp_try_send		  = lib.fatuv_udp_try_send
uv_udp_recv_start	  = lib.fatuv_udp_recv_start
uv_udp_recv_stop	  = lib.fatuv_udp_recv_stop
uv_udp_set_membership = lib.fatuv_udp_set_membership
uv_udp_set_multicast_loop  		= lib.fatuv_udp_set_multicast_loop
uv_udp_set_multicast_ttl 		= lib.fatuv_udp_set_multicast_ttl
uv_udp_set_multicast_interface	= lib.fatuv_udp_set_multicast_interface
uv_udp_set_broadcast 			= lib.fatuv_udp_set_broadcast
__all__ = ['UDP']

@ffi.def_extern()
def fatuv_udp_send_callback(handle, status):
	ptr = uv_get_pyobj(handle)
	obj = ffi.from_handle(ptr)
	obj._call_udp_send_callback(status)

@ffi.def_extern()
def fatuv_udp_recv_callback(handle, nread, buf, sockaddr, flags):
	ptr = uv_get_pyobj(handle)
	obj = ffi.from_handle(ptr)
	if nread < 0:
		obj._call_udp_recv_callback(None, nread, sockaddr, flags)
	elif nread > 0:
		data = ffi.unpack(buf.base, nread)
		obj._call_udp_recv_callback(data, nread, sockaddr, flags)
	else:
		obj._call_udp_recv_callback(None, nread, sockaddr, flags)

class UDP(Handle):
	def __init__(self, loop, flags=0):
		super(UDP, self).__init__(loop)

		handle = uv_udp_new()
		uv_udp_init(loop.handle, handle, flags)

		self._userdata = ffi.new_handle(self)
		uv_set_pyobj(handle, self._userdata)

		self.handle = handle

	def _dispose(self):
		handle = self.handle
		assert self.handle

		self.handle    = None
		self._userdata = None

		uv_set_pyobj(handle, ffi.NULL)
		uv_udp_delete(handle)

	def open(self, fd):
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		code = uv_udp_open(self.handle, fd)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def bind(self, addr, flags=0):
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		ip, port = addr
		ip = ffi.new('char[]', ip)
		code = uv_udp_v4_bind(self.handle, ip, port, flags)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def send(self,data,addr,callback=None):
		handle = self.handle
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		ip, port = addr
		ip = ffi.new('char[]', ip)
		self.send_callback = callback
		code = uv_udp_send(handle, data, len(data), ip, port, lib.fatuv_udp_send_callback)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def try_send(self, data, addr):
		handle = self.handle
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		ip, port = addr
		ip = ffi.new('char[]', ip)
		code = uv_udp_try_send(handle, data, len(data), ip, port)
		if code < 0:
			raise error.UVError(code)

	def _call_udp_send_callback(self,status):
		callback = self.send_callback
		if callback:
			callback(self,status)

	def receive_start(self,callback=None):
		handle = self.handle
		assert self.handle
		if self.closing:
			raise error.HandleClosedError()
		self.receive_callback = callback or self.receive_callback
		code = uv_udp_recv_start(self.handle, lib.fatuv_udp_recv_callback)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def _call_udp_recv_callback(self, data, error, sockaddr, flags):
		callback = self.receive_callback
		if callback:
			callback(self, data, error, sockaddr, flags)

	def receive_stop(self):
		if self.closing:
			return
		code = uv_udp_recv_stop(self.handle)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def set_membership(self, multicast_address, membership, interface_address=None):
		if self.closing:
			raise error.HandleClosedError()
		c_m_addr = multicast_address.encode()
		c_i_addr = interface_address.encode() if interface_address else ffi.NULL
		code = uv_udp_set_membership(self.handle, c_m_addr, c_i_addr, membership)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def set_multicast_loop(self, enable):
		if self.closing:
			raise error.HandleClosedError()
		code = uv_udp_set_multicast_loop(self.handle, int(enable))
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def set_multicast_ttl(self, ttl):
		if self.closing:
			raise error.HandleClosedError()
		code = uv_udp_set_multicast_ttl(self.handle, ttl)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def set_multicast_interface(self, interface):
		if self.closing:
			raise error.HandleClosedError()
		code = uv_udp_set_multicast_interface(self.handle, interface.encode())
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def set_broadcast(self, enable):
		if self.closing:
			raise error.HandleClosedError()
		code = uv_udp_set_broadcast(self.handle, int(enable))
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)
