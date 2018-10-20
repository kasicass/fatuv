from cffi import FFI
ffibuilder = FFI()


ffibuilder.cdef("""
	// struct uv_loop_t;

	// uv_loop_t* uv_default_loop(void);
	// int uv_run(uv_loop_t*, int mode);

	const char* uv_version_string(void);
""")


ffibuilder.set_source("_fatuv", """
	#include <uv.h>
""",
	include_dirs=['/usr/local/include'],
	library_dirs=['/usr/local/lib'],
	libraries=['uv'])


if __name__ == "__main__":
	ffibuilder.compile(verbose=True)

