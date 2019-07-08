#ifndef FATUV_WRAPPER_H
#define FATUV_WRAPPER_H

typedef struct fatuv_buf_s {
  char* base;
  size_t len;
} fatuv_buf_t;

typedef struct fatuv_addrinfo_s {
	int family;
	int socktype;
	int proto;
} fatuv_addrinfo_t;

typedef struct fatuv_timespec_s {
    long tv_sec;
    long tv_nsec;
} fatuv_timespec_t;

typedef struct fatuv_stat_s {
    uint64_t st_dev;
    uint64_t st_mode;
    uint64_t st_nlink;
    uint64_t st_uid;
    uint64_t st_gid;
    uint64_t st_rdev;
    uint64_t st_ino;
    uint64_t st_size;
    uint64_t st_blksize;
    uint64_t st_blocks;
    uint64_t st_flags;
    uint64_t st_gen;
    fatuv_timespec_t st_atim;
    fatuv_timespec_t st_mtim;
    fatuv_timespec_t st_ctim;
    fatuv_timespec_t st_birthtim;
} fatuv_stat_t;

typedef void fatuv_loop_t;
typedef void fatuv_handle_t;
typedef void fatuv_stream_t;
typedef void fatuv_tcp_t;
typedef void fatuv_tty_t;
typedef void fatuv_idle_t;
typedef void fatuv_check_t;
typedef void fatuv_prepare_t;
typedef void fatuv_timer_t;
typedef void fatuv_signal_t;
typedef void fatuv_getaddrinfo_t;
typedef void fatuv_pipe_t;
typedef void fatuv_async_t;
typedef void fatuv_fs_poll_t;
typedef void fatuv_fs_event_t;
typedef void fatuv_poll_t;
typedef void fatuv_shutdown_t;

typedef void (*fatuv_close_cb)(fatuv_handle_t* handle);
typedef void (*fatuv_connection_cb)(fatuv_stream_t* server, int status);
typedef void (*fatuv_idle_cb)(fatuv_idle_t* handle);
typedef void (*fatuv_timer_cb)(fatuv_timer_t* handle);
typedef void (*fatuv_signal_cb)(fatuv_signal_t* handle, int signum);
typedef void (*fatuv_read_cb)(fatuv_stream_t* stream, ssize_t nread, const fatuv_buf_t* buf);
typedef void (*fatuv_write_cb)(fatuv_stream_t* stream, int status);
typedef void (*fatuv_getaddrinfo_cb)(fatuv_addrinfo_t* result, int status);
typedef void (*fatuv_check_cb)(fatuv_check_t* handle);
typedef void (*fatuv_prepare_cb)(fatuv_prepare_t* handle);
typedef void (*fatuv_walk_cb)(fatuv_handle_t* handle,void* args);
typedef void (*fatuv_async_cb)(fatuv_async_t* handle);
typedef void (*fatuv_fs_poll_cb)(fatuv_fs_poll_t* handle, int stat, const fatuv_stat_t* uv_previous_stat,const fatuv_stat_t* uv_current_stat);
typedef void (*fatuv_fs_event_cb)(fatuv_fs_event_t* handle, const char* c_filename, int events, int status);
typedef void (*fatuv_poll_cb)(fatuv_poll_t* handle,  int status, int events);
typedef void (*fatuv_shutdown_cb)(fatuv_shutdown_t* req,  int status);

/*
 * misc
 */

const char* uv_strerror(int err);
const char* uv_err_name(int err);

/*
 * loop
 */

typedef enum {
	FATUV_RUN_DEFAULT = 0,
	FATUV_RUN_ONCE,
	FATUV_RUN_NOWAIT
} fatuv_run_mode;

fatuv_loop_t* fatuv_loop_new(void);
void fatuv_loop_delete(fatuv_loop_t* loop);

fatuv_loop_t* fatuv_default_loop(void);
int fatuv_loop_init(fatuv_loop_t* loop);
int fatuv_loop_close(fatuv_loop_t* loop);

int fatuv_run(fatuv_loop_t*, fatuv_run_mode mode);

void fatuv_walk(fatuv_loop_t*, fatuv_walk_cb walk_cb, void*);

/*
 * handle
 */

void fatuv_set_pyobj(fatuv_handle_t* handle, void* obj);
void* fatuv_get_pyobj(fatuv_handle_t* handle);

void fatuv_close(fatuv_handle_t* handle, fatuv_close_cb close_cb);
int fatuv_is_active(const fatuv_handle_t* handle);
int fatuv_is_closing(const fatuv_handle_t* handle);
int fatuv_send_buffer_size(fatuv_handle_t* handle, int* value);
int fatuv_recv_buffer_size(fatuv_handle_t* handle, int* value);
int fatuv_fileno(const fatuv_handle_t* handle, int* fd);

/*
 * buf
 */

// fatuv_buf_t* fatuv_buf_new(void);
// void fatuv_buf_delete(fatuv_buf_t* buf);

/*
 * stream
 */

int fatuv_listen(fatuv_stream_t* stream, int backlog, fatuv_connection_cb cb);
int fatuv_accept(fatuv_stream_t* server, fatuv_stream_t* client);
int fatuv_read_start(fatuv_stream_t* stream, fatuv_read_cb read_cb);
int fatuv_read_stop(fatuv_stream_t* stream);

int fatuv_write(fatuv_stream_t* stream, char* buf, unsigned int bufsz, fatuv_write_cb cb);
// int fatuv_write(fatuv_stream_t* stream, const fatuv_buf_t bufs[], unsigned int nbufs, fatuv_write_cb cb);

/*
int fatuv_write(uv_write_t* req, uv_stream_t* handle, const uv_buf_t bufs[], unsigned int nbufs, uv_write_cb cb);
*/

/*
 * tcp
 */

fatuv_tcp_t* fatuv_tcp_new(void);
void fatuv_tcp_delete(fatuv_tcp_t* handle);

int fatuv_tcp_init(fatuv_loop_t* loop, fatuv_tcp_t* handle);
int fatuv_tcp_nodelay(fatuv_tcp_t* handle, int enable);
int fatuv_tcp_keepalive(fatuv_tcp_t* handle, int enable, unsigned int delay);
int fatuv_tcp_v4_bind(fatuv_tcp_t* handle, const char* ip, int port);
int fatuv_tcp_v4_getpeername(const fatuv_tcp_t* handle, char* ip, int* port);

/*
 * idle
 */

fatuv_idle_t* fatuv_idle_new(void);
void fatuv_idle_delete(fatuv_idle_t* idle);

int fatuv_idle_init(fatuv_loop_t* loop, fatuv_idle_t* idle);
int fatuv_idle_start(fatuv_idle_t* idle, fatuv_idle_cb cb);
int fatuv_idle_stop(fatuv_idle_t* idle);

/*
 * timer
 */

fatuv_timer_t* fatuv_timer_new(void);
void fatuv_timer_delete(fatuv_timer_t* timer);

int fatuv_timer_init(fatuv_loop_t* loop, fatuv_timer_t* timer);
int fatuv_timer_start(fatuv_timer_t* timer, fatuv_timer_cb cb, uint64_t timeout, uint64_t repeat);
int fatuv_timer_stop(fatuv_timer_t* timer);
int fatuv_timer_again(fatuv_timer_t* timer);
void fatuv_timer_set_repeat(fatuv_timer_t* timer, uint64_t repeat);
uint64_t fatuv_timer_get_repeat(const fatuv_timer_t* timer);

/*
 * signal
 */

fatuv_signal_t* fatuv_signal_new(void);
void fatuv_signal_delete(fatuv_signal_t* signal);

int fatuv_signal_init(fatuv_loop_t* loop, fatuv_signal_t* signal);
int fatuv_signal_start(fatuv_signal_t* signal, fatuv_signal_cb signal_cb, int signum);
//int fatuv_signal_start_oneshot(fatuv_signal_t* signal, fatuv_signal_cb signal_cb, int signum);
int fatuv_signal_stop(fatuv_signal_t* signal);

/*
 * dns
 */

int fatuv_getaddrinfo(fatuv_loop_t* loop, fatuv_getaddrinfo_cb getaddrinfo_cb, const char* node, const char* service);

//int fatuv_getnameinfo(fatuv_loop_t* loop, fatuv_getaddrinfo_cb getaddrinfo_cb, const char* node, const char* service);

/*
 * check
 */

fatuv_check_t* fatuv_check_new(void);
void fatuv_check_delete(fatuv_check_t* check);

int fatuv_check_init(fatuv_loop_t* loop, fatuv_check_t* check);
int fatuv_check_start(fatuv_check_t* check, fatuv_check_cb cb);
int fatuv_check_stop(fatuv_check_t* check);

/*
 * prepare
 */

fatuv_prepare_t* fatuv_prepare_new(void);
void fatuv_prepare_delete(fatuv_prepare_t* prepare);

int fatuv_prepare_init(fatuv_loop_t* loop, fatuv_prepare_t* prepare);
int fatuv_prepare_start(fatuv_prepare_t* prepare, fatuv_prepare_cb cb);
int fatuv_prepare_stop(fatuv_prepare_t* prepare);

void fatuv_ref(fatuv_handle_t* handle);
void fatuv_unref(fatuv_handle_t* handle);
int fatuv_has_ref(fatuv_handle_t* handle);

/*
 * tty
 */
typedef enum {
    FATUV_TTY_MODE_NORMAL,
    FATUV_TTY_MODE_RAW,
    FATUV_TTY_MODE_IO
} fatuv_tty_mode;

fatuv_tty_t* fatuv_tty_new(void);
void fatuv_tty_delete(fatuv_tty_t* handle);
int fatuv_tty_init(fatuv_loop_t* loop, fatuv_tty_t* handle, int fd, int readable);
int fatuv_tty_set_mode(fatuv_tty_t* handle, fatuv_tty_mode mode);
int fatuv_tty_reset_mode(void);
int fatuv_tty_get_winsize(fatuv_tty_t* handle, int* c_with, int* c_height);

/*
 * pipe
 */

fatuv_pipe_t* fatuv_pipe_new(void);
void fatuv_pipe_delete(fatuv_pipe_t* handle);
int fatuv_pipe_init(fatuv_loop_t* loop, fatuv_pipe_t* handle, int ipc);
int fatuv_pipe_open(fatuv_pipe_t* handle, int fd);
int fatuv_pipe_bind(fatuv_pipe_t* handle, char* pipeName);

/*
 * async
 */

fatuv_async_t* fatuv_async_new(void);
int fatuv_async_init(fatuv_loop_t* loop, fatuv_async_t* handle, fatuv_async_cb cb);
void fatuv_async_delete(fatuv_async_t* handle);
int fatuv_async_send(fatuv_async_t* handle);

/*
 * fs_poll
 */

fatuv_fs_poll_t* fatuv_fs_poll_new(void);
int fatuv_fs_poll_init(fatuv_loop_t* loop, fatuv_fs_poll_t* handle);
void fatuv_fs_poll_delete(fatuv_fs_poll_t* handle);
int fatuv_fs_poll_start(fatuv_fs_poll_t* handle, fatuv_fs_poll_cb cb, char* path, int interval);
int fatuv_fs_poll_stop(fatuv_fs_poll_t* handle);

/*
 * fs_event
 */

typedef enum {
    FATUV_FS_EVENTS_RENAME = 1,
    FATUV_FS_EVENTS_CHANGE,
    FATUV_FS_EVENTS_MODE_IO
} fatuv_fs_events;

typedef enum {
    FATUV_FS_EVENT_FLAGS_WATCH_ENTRY = 1,
    FATUV_FS_EVENT_FLAGS_STAT,
    FATUV_FS_EVENT_FLAGS_RECURSIVE
} fatuv_fs_event_flags;

fatuv_fs_event_t* fatuv_fs_event_new(void);
int fatuv_fs_event_init(fatuv_loop_t* loop, fatuv_fs_event_t* handle);
void fatuv_fs_event_delete(fatuv_fs_event_t* handle);
int fatuv_fs_event_start(fatuv_fs_event_t* handle, fatuv_fs_event_cb cb, char* path, unsigned int flags);
int fatuv_fs_event_stop(fatuv_fs_event_t* handle);

/*
 * poll
 */
typedef enum {
    FATUV_POLL_EVENT_READABLE = 1,
    FATUV_POLL_EVENT_WRITABLE
} fatuv_poll_events;

fatuv_poll_t* fatuv_poll_new(void);
int fatuv_poll_init(fatuv_loop_t* loop, fatuv_poll_t* handle, int fd);
void fatuv_poll_delete(fatuv_poll_t* handle);
int fatuv_poll_start(fatuv_poll_t* handle, int status, fatuv_poll_cb cb);
int fatuv_poll_stop(fatuv_poll_t* handle);

/*
 * shutdown
 */
int fatuv_shutdown(fatuv_stream_t* stream, fatuv_shutdown_cb cb);

#endif
