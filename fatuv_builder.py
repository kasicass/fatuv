from cffi import FFI
ffibuilder = FFI()


ffibuilder.cdef("""
	typedef enum {
		UV_RUN_DEFAULT = 0,
		UV_RUN_ONCE,
		UV_RUN_NOWAIT
	} uv_run_mode;

	void* uv_default_loop(void);
	int uv_run(void*, uv_run_mode mode);

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

