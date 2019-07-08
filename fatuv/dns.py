import sys
from _fatuv import ffi, lib
from .handle import Handle

uv_getaddrinfo = lib.fatuv_getaddrinfo
#uv_getnameinfo = lib.fatuv_getnameinfo

__all__ = ['getaddrinfo']

def getaddrinfo(loop, node, service, callback):
	if isinstance(service, int):
		service = str(service)

	uv_getaddrinfo(loop.handle, node, service, callback)


#def getnameinfo():
#	uv_getnameinfo()