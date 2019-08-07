from _fatuv import ffi, lib
from fatuv import Loop
import socket

uv_get_pyobj  = lib.fatuv_get_pyobj
uv_set_pyobj  = lib.fatuv_set_pyobj
uv_getaddrinfo_ctx_new = lib.fatuv_getaddrinfo_ctx_new
uv_getaddrinfo_ctx_delete = lib.fatuv_getaddrinfo_ctx_delete
uv_getaddrinfo = lib.fatuv_getaddrinfo
#uv_getnameinfo = lib.fatuv_getnameinfo

__all__ = ['getaddrinfo']

def getaddrinfo(loop, node, service, callback):
	if isinstance(service, int):
		service = str(service)
	GetAddrInfo(node,service,callback,loop=loop)

@ffi.def_extern()
def fatuv_getaddrinfo_callback(req, addrinfo_request, status):
	ptr = uv_get_pyobj(req)
	obj = ffi.from_handle(ptr)
	obj._call_getaddrinfo_callback(addrinfo_request, status)

class AddrInfo(tuple):
	__slots__ = []

	def __new__(cls, family, socktype, protocol, canonname, address):
		return tuple.__new__(cls, (family,socktype,protocol,canonname, address))

	def __repr__(self):
		return ('<AddressInfo family={self.family!r}, type={self.socktype!r}, '
				'protocol={self.protocol!r}, canonname="{self.canonname}", '
				'address={self.address!r}>').format(self=self)

	@property
	def family(self):
		return self[0]

	@property
	def socktype(self):
		return self[1]

	@property
	def protocol(self):
		return self[2]

	@property
	def canonname(self):
		return self[3]

	@property
	def address(self):
		return self[4]

class Address(tuple):
	__slots__ = []
	def __new__(cls, host, port):
		return tuple.__new__(cls, (host, port))

	@property
	def host(self):
		return self[0]

	@property
	def port(self):
		return self[1]

class Address4(Address):
	__slots__ = []
	family = socket.AF_INET
	def __repr__(self):
		return '<Address4 host="{self.host}", port={self.port}>'.format(self=self)

def unpack_sockaddr(c_sockaddr):
	if c_sockaddr.sa_family == socket.AF_INET:
		c_sockaddr_in4 = ffi.cast('struct fatuv_sockaddr_in*', c_sockaddr)
		c_host = ffi.new('char[16]')
		port = socket.ntohs(c_sockaddr_in4.sin_port)
		lib.fatuv_ip4_name(c_sockaddr_in4, c_host, 16)
		return Address4(ffi.string(c_host).decode(), port)
	elif c_sockaddr.sa_family == socket.AF_INET6:
		#not support
		return None

def unpack_addrinfo(c_addrinfo):
	items, c_next = [], c_addrinfo
	while c_next:
		family = c_next.ai_family
		socktype = c_next.ai_socktype
		protocol = c_next.ai_protocol
		if c_next.ai_canonname:
			canonname = ffi.string(c_next.ai_canonname).decode()
		else:
			canonname = None
		address = unpack_sockaddr(c_next.ai_addr) if c_next.ai_addr else None
		items.append(AddrInfo(family, socktype, protocol, canonname, address))
		c_next = c_next.ai_next
	return items

class GetAddrInfo(object):
	def __init__(self, node, service, callback, loop=None):
		self.loop           = loop or Loop.default_loop()
		request = uv_getaddrinfo_ctx_new()
		self.request = request
		self._userdata = ffi.new_handle(self)
		uv_set_pyobj(request, self._userdata)
		self.get_addrinfo_callback = callback

		c_hints = ffi.new('struct fatuv_addrinfo_s*')
		c_hints.ai_family = socket.AF_INET
		c_hints.ai_socktype = socket.SOCK_STREAM
		c_hints.ai_protocol = socket.IPPROTO_TCP
		c_hints.ai_flags = 0

		uv_getaddrinfo(loop.handle, request, lib.fatuv_getaddrinfo_callback, node, service, c_hints)
		self.set_pending()

	def set_pending(self):
		self.loop.set_pending(self)

	def clear_pending(self):
		self.loop.clear_pending(self)

	def _call_getaddrinfo_callback(self,addrinfo_request,status):
		callback = self.get_addrinfo_callback
		self.clear_pending()
		if callback:
			self.get_addrinfo_callback = None
			addrinfo = unpack_addrinfo(addrinfo_request)
			callback(addrinfo,status)

		self._dispose()

	def _dispose(self):
		request = self.request
		assert request

		self.get_addrinfo_callback = None
		self.request         = None
		self._userdata      = None

		uv_set_pyobj(request, ffi.NULL)
		uv_getaddrinfo_ctx_delete(request)