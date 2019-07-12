from _fatuv import ffi, lib

uv_strerror = lib.uv_strerror
uv_err_name = lib.uv_err_name

__all__ = ['get_strerror', 'get_err_name']

def get_strerror(err):
	ptr = uv_strerror(err)
	return ffi.string(ptr)

def get_err_name(err):
	ptr = uv_err_name(err)
	return ffi.string(ptr)

