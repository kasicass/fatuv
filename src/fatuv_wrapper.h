#ifndef FATUV_WRAPPER_H
#define FATUV_WRAPPER_H

typedef void fatuv_loop_t;
typedef void fatuv_handle_t;
typedef void fatuv_stream_t;
typedef void fatuv_tcp_t;
typedef void fatuv_idle_t;
typedef void fatuv_timer_t;
typedef void fatuv_signal_t;

typedef void (*fatuv_close_cb)(fatuv_handle_t* handle);
typedef void (*fatuv_connection_cb)(fatuv_stream_t* server, int status);
typedef void (*fatuv_idle_cb)(fatuv_idle_t* handle);
typedef void (*fatuv_timer_cb)(fatuv_timer_t* handle);
typedef void (*fatuv_signal_cb)(fatuv_signal_t* handle, int signum);

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

/*
 * handle
 */

void fatuv_close(fatuv_handle_t* handle, fatuv_close_cb close_cb);
int fatuv_is_active(const fatuv_handle_t* handle);
int fatuv_is_closing(const fatuv_handle_t* handle);
int fatuv_send_buffer_size(fatuv_handle_t* handle, int* value);
int fatuv_recv_buffer_size(fatuv_handle_t* handle, int* value);

/* stream */
int fatuv_listen(fatuv_stream_t* stream, int backlog, fatuv_connection_cb cb);
/*
int fatuv_accept(uv_stream_t* server, uv_stream_t* client);
int fatuv_read_start(uv_stream_t*, uv_alloc_cb alloc_cb, uv_read_cb read_cb);
int fatuv_read_stop(uv_stream_t*);
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
void fatuv_timer_delete(fatuv_timer_t* handle);

int fatuv_timer_init(fatuv_loop_t* loop, fatuv_timer_t* handle);
int fatuv_timer_start(fatuv_timer_t* handle, fatuv_timer_cb cb, uint64_t timeout, uint64_t repeat);
int fatuv_timer_stop(fatuv_timer_t* handle);
int fatuv_timer_again(fatuv_timer_t* handle);
void fatuv_timer_set_repeat(fatuv_timer_t* handle, uint64_t repeat);
uint64_t fatuv_timer_get_repeat(const fatuv_timer_t* handle);

/*
 * signal
 */

fatuv_signal_t* fatuv_signal_new(void);
void fatuv_signal_delete(fatuv_signal_t* handle);

int fatuv_signal_init(fatuv_loop_t* loop, fatuv_signal_t* handle);
int fatuv_signal_start(fatuv_signal_t* handle, fatuv_signal_cb signal_cb, int signum);
//int fatuv_signal_start_oneshot(fatuv_signal_t* handle, fatuv_signal_cb signal_cb, int signum);
int fatuv_signal_stop(fatuv_signal_t* handle);

#endif
