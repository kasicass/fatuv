from cffi import FFI
import os
import sys
ffibuilder = FFI()

include_file = open('fatuv_wrapper.h', 'r')
data = include_file.read()
include_file.close()

data = data[48:] # remove FATUV_WRAPPER_H
data = data[:-8] # remove #endif

data += """
extern "Python" void fatuv_close_callback(fatuv_handle_t*);
extern "Python" void fatuv_connection_callback(fatuv_stream_t*, int status);
extern "Python" void fatuv_idle_callback(fatuv_idle_t*);
extern "Python" void fatuv_timer_callback(fatuv_timer_t*);
extern "Python" void fatuv_signal_callback(fatuv_signal_t*, int signum);
extern "Python" void fatuv_read_callback(fatuv_stream_t* stream, ssize_t nread, const fatuv_buf_t* buf);
extern "Python" void fatuv_write_callback(fatuv_stream_t* stream, int status, void* userdata);
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
extern "Python" void fatuv_pipe_connect_cb(fatuv_pipe_t*, int);
extern "Python" void fatuv_tcp_connect_cb(fatuv_tcp_t*, int);
extern "Python" void fatuv_exit_callback(fatuv_process_t*, int64_t, int);
extern "Python" void fatuv_getaddrinfo_callback(fatuv_getaddrinfo_t*, fatuv_addrinfo_t*, int);
"""

def read_source(name):
    with open(name, 'r') as f:
        return f.read()

_source = read_source('fatuv_wrapper.c')

def _libuv_source(rel_path):
    path = os.path.join('../', 'libuv', 'src', rel_path)
    return path

LIBUV_SOURCES = [
    _libuv_source('fs-poll.c'),
    _libuv_source('inet.c'),
    _libuv_source('threadpool.c'),
    _libuv_source('uv-common.c'),
    _libuv_source('version.c'),
    _libuv_source('uv-data-getter-setters.c'),
    _libuv_source('timer.c'),
    _libuv_source('idna.c'),
    _libuv_source('strscpy.c')
]

LIBUV_SOURCES += [
    _libuv_source('unix/async.c'),
    _libuv_source('unix/core.c'),
    _libuv_source('unix/dl.c'),
    _libuv_source('unix/fs.c'),
    _libuv_source('unix/getaddrinfo.c'),
    _libuv_source('unix/getnameinfo.c'),
    _libuv_source('unix/loop-watcher.c'),
    _libuv_source('unix/loop.c'),
    _libuv_source('unix/pipe.c'),
    _libuv_source('unix/poll.c'),
    _libuv_source('unix/process.c'),
    _libuv_source('unix/signal.c'),
    _libuv_source('unix/stream.c'),
    _libuv_source('unix/tcp.c'),
    _libuv_source('unix/thread.c'),
    _libuv_source('unix/tty.c'),
    _libuv_source('unix/udp.c'),
]

LIBUV_SOURCES += [
    _libuv_source('unix/linux-core.c'),
    _libuv_source('unix/linux-inotify.c'),
    _libuv_source('unix/linux-syscalls.c'),
    _libuv_source('unix/procfs-exepath.c'),
    _libuv_source('unix/proctitle.c'),
    _libuv_source('unix/sysinfo-loadavg.c'),
]

libuv_dir = os.path.abspath(os.path.join('../', 'libuv'))
LIBUV_INCLUDE_DIRS = [
    os.path.join(libuv_dir, 'include'),
    os.path.join(libuv_dir, 'src'),
]

LIBUV_LIBRARIES = []
def _add_library(name):
    LIBUV_LIBRARIES.append(name)

LIBUV_EMBED=False
LIBUV_MACROS = [
    ('LIBUV_EMBED', int(LIBUV_EMBED)),
]


def _define_macro(name, value):
    LIBUV_MACROS.append((name, value))

if sys.platform != 'win32':
    _define_macro('_LARGEFILE_SOURCE', 1)
    _define_macro('_FILE_OFFSET_BITS', 64)

if sys.platform.startswith('linux'):
    _add_library('dl')
    _add_library('rt')
    _define_macro('_GNU_SOURCE', 1)
    _define_macro('_POSIX_C_SOURCE', '200112')

ffibuilder.cdef(data)
ffibuilder.set_source("_fatuv", 
	_source,
	extra_compile_args=['-g'],
	sources=LIBUV_SOURCES,
	depends=LIBUV_SOURCES,
	include_dirs=LIBUV_INCLUDE_DIRS,
	libraries=list(LIBUV_LIBRARIES),
	define_macros=list(LIBUV_MACROS)
	)


if __name__ == "__main__":
	ffibuilder.compile(verbose=True)

