#include <stdlib.h>
#include <uv.h>
#include "fatuv_wrapper.h"

/*
 * loop
 */

fatuv_loop_t*
fatuv_loop_new(void)
{
	return (fatuv_loop_t*)malloc(sizeof(uv_loop_t));
}

void
fatuv_loop_delete(fatuv_loop_t* loop)
{
	free(loop);
}

fatuv_loop_t*
fatuv_default_loop(void)
{
	return (fatuv_loop_t*)uv_default_loop();
}

int
fatuv_loop_init(fatuv_loop_t* loop)
{
	return uv_loop_init((uv_loop_t*)loop);
}

int
fatuv_loop_close(fatuv_loop_t* loop)
{
	return uv_loop_close((uv_loop_t*)loop);
}

int
fatuv_run(fatuv_loop_t* loop, fatuv_run_mode mode)
{
	return uv_run((uv_loop_t*)loop, (uv_run_mode)mode);
}

/*
 * handle
 */
void
fatuv_close(fatuv_handle_t* handle, fatuv_close_cb close_cb)
{
	uv_close((uv_handle_t*)handle, (uv_close_cb)close_cb);
}

int
fatuv_is_active(const fatuv_handle_t* handle)
{
	return uv_is_active((const uv_handle_t*)handle);
}

int
fatuv_is_closing(const fatuv_handle_t* handle)
{
	return uv_is_closing((const uv_handle_t*)handle);
}

int
fatuv_send_buffer_size(fatuv_handle_t* handle, int* value)
{
	return uv_send_buffer_size((uv_handle_t*)handle, value);
}

int
fatuv_recv_buffer_size(fatuv_handle_t* handle, int* value)
{
	return uv_recv_buffer_size((uv_handle_t*)handle, value);
}

int
fatuv_fileno(const fatuv_handle_t* handle, int* fd)
{
	return uv_fileno((uv_handle_t*)handle, fd);
}

/*
 * stream
 */

int
fatuv_listen(fatuv_stream_t* stream, int backlog, fatuv_connection_cb cb)
{
	return uv_listen((uv_stream_t*)stream, backlog, (uv_connection_cb)cb);
}

int
fatuv_accept(fatuv_stream_t* server, fatuv_stream_t* client)
{
	return uv_accept((uv_stream_t*)server, (uv_stream_t*)client);
}

static void
fatuv_alloc_cb(uv_handle_t *handle, size_t suggested_size, uv_buf_t *buf)
{
	static char slab[64*1024];
	buf->base = slab;
	buf->len  = sizeof(slab);
}

int
fatuv_read_start(fatuv_stream_t* stream, fatuv_read_cb read_cb)
{
	return uv_read_start((uv_stream_t*)stream, fatuv_alloc_cb, (uv_read_cb)read_cb);
}

int
fatuv_read_stop(fatuv_stream_t* stream)
{
	return uv_read_stop((uv_stream_t*)stream);
}

/*
 * tcp
 */

fatuv_tcp_t*
fatuv_tcp_new(void)
{
	return (fatuv_tcp_t*)malloc(sizeof(uv_tcp_t));
}

void fatuv_tcp_delete(fatuv_tcp_t* handle)
{
	free(handle);
}

int
fatuv_tcp_init(fatuv_loop_t* loop, fatuv_tcp_t* handle)
{
	return uv_tcp_init((uv_loop_t*)loop, (uv_tcp_t*)handle);
}

int
fatuv_tcp_nodelay(fatuv_tcp_t* handle, int enable)
{
	return uv_tcp_nodelay((uv_tcp_t*)handle, enable);
}

int
fatuv_tcp_keepalive(fatuv_tcp_t* handle, int enable, unsigned int delay)
{
	return uv_tcp_keepalive((uv_tcp_t*)handle, enable, delay);
}

int
fatuv_tcp_v4_bind(fatuv_tcp_t* handle, const char* ip, int port)
{
	struct sockaddr_in addr;
	uv_ip4_addr(ip, port, &addr);
	return uv_tcp_bind((uv_tcp_t*)handle, (const struct sockaddr*)&addr, 0);
}

int
fatuv_tcp_v4_getpeername(const fatuv_tcp_t* handle, char* ip, int* port)
{
	// ip = char[16]
	int err, namelen;
	struct sockaddr_storage peername;
	struct sockaddr_in *addr4;

	namelen = sizeof(peername);

	err = uv_tcp_getpeername((uv_tcp_t*)handle, (struct sockaddr *)&peername, &namelen);
	if (err < 0) {
		return err;
	}

	addr4 = (struct sockaddr_in*)&peername;
	uv_ip4_name(addr4, ip, INET_ADDRSTRLEN); // INET_ADDRSTRLEN = 16
	*port = ntohs(addr4->sin_port);
	return 0;
}

/*
 * idle
 */

typedef struct fatuv_idle_internal_s {
	uv_idle_t handle;
	void* pyobj;
} fatuv_idle_internal_t;

fatuv_idle_t*
fatuv_idle_new(void)
{
	return (fatuv_idle_t*)calloc(1, sizeof(fatuv_idle_internal_t));
}

void
fatuv_idle_delete(fatuv_idle_t* idle)
{
	free(idle);
}

void
fatuv_idle_set_pyobj(fatuv_idle_t* idle, void* obj)
{
	fatuv_idle_internal_t* self = (fatuv_idle_internal_t*)idle;
	self->pyobj = obj;
}

void*
fatuv_idle_get_pyobj(fatuv_idle_t* idle)
{
	fatuv_idle_internal_t* self = (fatuv_idle_internal_t*)idle;
	return self->pyobj;
}

int
fatuv_idle_init(fatuv_loop_t* loop, fatuv_idle_t* idle)
{
	return uv_idle_init((uv_loop_t*)loop, (uv_idle_t*)idle);
}

int
fatuv_idle_start(fatuv_idle_t* idle, fatuv_idle_cb cb)
{
	return uv_idle_start((uv_idle_t*)idle, (uv_idle_cb)cb);
}

int
fatuv_idle_stop(fatuv_idle_t* idle)
{
	return uv_idle_stop((uv_idle_t*)idle);
}

/*
 * timer
 */

fatuv_timer_t*
fatuv_timer_new(void)
{
	return (fatuv_timer_t*)malloc(sizeof(uv_timer_t));
}

void
fatuv_timer_delete(fatuv_timer_t* handle)
{
	free(handle);
}

int
fatuv_timer_init(fatuv_loop_t* loop, fatuv_timer_t* handle)
{
	return uv_timer_init((uv_loop_t*)loop, (uv_timer_t*)handle);
}

int
fatuv_timer_start(fatuv_timer_t* handle, fatuv_timer_cb cb, uint64_t timeout, uint64_t repeat)
{
	return uv_timer_start((uv_timer_t*)handle, (uv_timer_cb)cb, timeout, repeat);
}

int
fatuv_timer_stop(fatuv_timer_t* handle)
{
	return uv_timer_stop((uv_timer_t*)handle);
}

int
fatuv_timer_again(fatuv_timer_t* handle)
{
	return uv_timer_again((uv_timer_t*)handle);
}

void
fatuv_timer_set_repeat(fatuv_timer_t* handle, uint64_t repeat)
{
	uv_timer_set_repeat((uv_timer_t*)handle, repeat);
}

uint64_t
fatuv_timer_get_repeat(const fatuv_timer_t* handle)
{
	return uv_timer_get_repeat((uv_timer_t*)handle);
}

/*
 * signal
 */

fatuv_signal_t*
fatuv_signal_new(void)
{
	return (fatuv_signal_t*)malloc(sizeof(uv_signal_t));
}

void
fatuv_signal_delete(fatuv_signal_t* handle)
{
	free(handle);
}

int
fatuv_signal_init(fatuv_loop_t* loop, fatuv_signal_t* handle)
{
	return uv_signal_init((uv_loop_t*)loop, (uv_signal_t*)handle);
}

int
fatuv_signal_start(fatuv_signal_t* handle, fatuv_signal_cb signal_cb, int signum)
{
	return uv_signal_start((uv_signal_t*)handle, (uv_signal_cb)signal_cb, signum);
}

#if 0  // debian9.5 libuv1-dev package is too old
int
fatuv_signal_start_oneshot(fatuv_signal_t* handle, fatuv_signal_cb signal_cb, int signum)
{
	return uv_signal_start_oneshot((uv_signal_t*)handle, (uv_signal_cb)signal_cb, signum);
}
#endif

int
fatuv_signal_stop(fatuv_signal_t* handle)
{
	return uv_signal_stop((uv_signal_t*)handle);
}

