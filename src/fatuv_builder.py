from cffi import FFI
ffibuilder = FFI()

include_file = open('fatuv_wrapper.h', 'r')
data = include_file.read()
include_file.close()

data = data[48:] # remove FATUV_WRAPPER_H
data = data[:-7] # remove #endif

data += """
extern "Python" void fatuv_close_callback(fatuv_handle_t*);
extern "Python" void fatuv_connection_callback(fatuv_stream_t*, int status);
extern "Python" void fatuv_idle_callback(fatuv_idle_t*);
extern "Python" void fatuv_timer_callback(fatuv_timer_t*);
extern "Python" void fatuv_signal_callback(fatuv_signal_t*, int signum);
"""


ffibuilder.cdef(data)
ffibuilder.set_source("_fatuv", """
	#include "fatuv_wrapper.h"
""",
	include_dirs=['/usr/local/include'],
	library_dirs=['/usr/local/lib'],
	sources=['fatuv_wrapper.c'],
	libraries=['uv'])


if __name__ == "__main__":
	ffibuilder.compile(verbose=True)

