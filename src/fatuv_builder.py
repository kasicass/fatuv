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
extern "Python" void fatuv_read_callback(fatuv_stream_t* stream, ssize_t nread, const fatuv_buf_t* buf);
extern "Python" void fatuv_write_callback(fatuv_stream_t* stream, int status);
extern "Python" void fatuv_check_callback(fatuv_check_t*);
extern "Python" void fatuv_prepare_callback(fatuv_prepare_t*);
extern "Python" void fatuv_walk_callback(fatuv_handle_t*,void*);
extern "Python" void fatuv_async_callback(fatuv_check_t*);
extern "Python" void fatuv_fs_poll_callback(fatuv_fs_poll_t*, int, const fatuv_stat_t*, const fatuv_stat_t*);
extern "Python" void fatuv_fs_event_callback(fatuv_fs_event_t*, const char*, int, int);
extern "Python" void fatuv_poll_callback(fatuv_poll_t*, int, int);
extern "Python" void fatuv_shutdown_callback(fatuv_shutdown_t*, int);
extern "Python" void fatuv_udp_send_callback(fatuv_udp_t*, int);
extern "Python" void fatuv_udp_recv_callback(fatuv_udp_t* handle, ssize_t nread, const fatuv_buf_t* buf, const void* addr, unsigned flags);
"""


ffibuilder.cdef(data)
ffibuilder.set_source("_fatuv", """
	#include "fatuv_wrapper.h"
""",
#	extra_compile_args=['-g'],
	include_dirs=['../libuv/include'],
	library_dirs=['../libuv/.libs'],
	sources=['fatuv_wrapper.c'],
	libraries=['uv'])


if __name__ == "__main__":
	ffibuilder.compile(verbose=True)

