from _fatuv import ffi, lib

def uv_version_string():
	return lib.uv_version_string()

