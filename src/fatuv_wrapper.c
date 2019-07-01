#include <stdlib.h>
#include <uv.h>
#include "fatuv_wrapper.h"

#define FATUV_PYOBJ_FIELDS void* pyobj
#define FAT2UV_HANDLE(type, ptr) ((type)(ptr + sizeof(void*)))
#define UV2FAT_HANDLE(type, ptr) ((type)(ptr - sizeof(void*)))

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

typedef struct fatuv_handle_internal_s {
	FATUV_PYOBJ_FIELDS;
} fatuv_handle_internal_t;

void
fatuv_set_pyobj(fatuv_handle_t* handle, void* obj)
{
	fatuv_handle_internal_t* self = (fatuv_handle_internal_t*)handle;
	self->pyobj = obj;
}

void*
fatuv_get_pyobj(fatuv_handle_t* handle)
{
	fatuv_handle_internal_t* self = UV2FAT_HANDLE(fatuv_handle_internal_t*, handle);
	return self->pyobj;
}

void
fatuv_close(fatuv_handle_t* handle, fatuv_close_cb close_cb)
{
	uv_close(FAT2UV_HANDLE(uv_handle_t*, handle), (uv_close_cb)close_cb);
}

int
fatuv_is_active(const fatuv_handle_t* handle)
{
	return uv_is_active(FAT2UV_HANDLE(const uv_handle_t*, handle));
}

int
fatuv_is_closing(const fatuv_handle_t* handle)
{
	return uv_is_closing(FAT2UV_HANDLE(const uv_handle_t*, handle));
}

int
fatuv_send_buffer_size(fatuv_handle_t* handle, int* value)
{
	return uv_send_buffer_size(FAT2UV_HANDLE(uv_handle_t*, handle), value);
}

int
fatuv_recv_buffer_size(fatuv_handle_t* handle, int* value)
{
	return uv_recv_buffer_size(FAT2UV_HANDLE(uv_handle_t*, handle), value);
}

int
fatuv_fileno(const fatuv_handle_t* handle, int* fd)
{
	return uv_fileno(FAT2UV_HANDLE(uv_handle_t*, handle), fd);
}

/*
 * stream
 */

int
fatuv_listen(fatuv_stream_t* stream, int backlog, fatuv_connection_cb cb)
{
	return uv_listen(FAT2UV_HANDLE(uv_stream_t*, stream), backlog, (uv_connection_cb)cb);
}

int
fatuv_accept(fatuv_stream_t* server, fatuv_stream_t* client)
{
	return uv_accept(FAT2UV_HANDLE(uv_stream_t*, server), FAT2UV_HANDLE(uv_stream_t*, client));
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
	return uv_read_start(FAT2UV_HANDLE(uv_stream_t*, stream), fatuv_alloc_cb, (uv_read_cb)read_cb);
}

int
fatuv_read_stop(fatuv_stream_t* stream)
{
	return uv_read_stop(FAT2UV_HANDLE(uv_stream_t*, stream));
}

/*
 * stream-write
 */

typedef struct fatuv_write_ctx_s {
	uv_write_t req;
	fatuv_stream_t* fatstream;
	fatuv_write_cb callback;
} fatuv_write_ctx_t;

static fatuv_write_ctx_t*
fatuv_write_ctx_new(void)
{
	return (fatuv_write_ctx_t*)calloc(1, sizeof(fatuv_write_ctx_t));
}

static void
fatuv_write_ctx_delete(fatuv_write_ctx_t* ctx)
{
	free(ctx);
}

static void
fatuv_write_callback_internal(uv_write_t *req, int status)
{
	fatuv_write_ctx_t *ctx;

	ctx = (fatuv_write_ctx_t*)req;
	ctx->callback(ctx->fatstream, status);

	fatuv_write_ctx_delete(ctx);
}

int
fatuv_write(fatuv_stream_t* fatstream, char* buf, unsigned int bufsz, fatuv_write_cb cb)
{
	uv_stream_t* stream;
	fatuv_write_ctx_t *ctx;
	uv_buf_t wrbuf;
	
	stream = FAT2UV_HANDLE(uv_stream_t*, fatstream);
	ctx = fatuv_write_ctx_new();

	ctx->fatstream = stream;
	ctx->callback  = cb;

	wrbuf = uv_buf_init(buf, bufsz);
	return uv_write((uv_write_t*)ctx, stream, &wrbuf, 1, fatuv_write_callback_internal);
}

/*
 * tcp
 */

typedef struct fatuv_tcp_internal_s {
	FATUV_PYOBJ_FIELDS;
	uv_tcp_t handle;
} fatuv_tcp_internal_t;

fatuv_tcp_t*
fatuv_tcp_new(void)
{
	return (fatuv_tcp_t*)calloc(1, sizeof(fatuv_tcp_internal_t));
}

void fatuv_tcp_delete(fatuv_tcp_t* handle)
{
	free(handle);
}

int
fatuv_tcp_init(fatuv_loop_t* loop, fatuv_tcp_t* handle)
{
	return uv_tcp_init((uv_loop_t*)loop, FAT2UV_HANDLE(uv_tcp_t*, handle));
}

int
fatuv_tcp_nodelay(fatuv_tcp_t* handle, int enable)
{
	return uv_tcp_nodelay(FAT2UV_HANDLE(uv_tcp_t*, handle), enable);
}

int
fatuv_tcp_keepalive(fatuv_tcp_t* handle, int enable, unsigned int delay)
{
	return uv_tcp_keepalive(FAT2UV_HANDLE(uv_tcp_t*, handle), enable, delay);
}

int
fatuv_tcp_v4_bind(fatuv_tcp_t* handle, const char* ip, int port)
{
	struct sockaddr_in addr;
	uv_ip4_addr(ip, port, &addr);
	return uv_tcp_bind(FAT2UV_HANDLE(uv_tcp_t*, handle), (const struct sockaddr*)&addr, 0);
}

int
fatuv_tcp_v4_getpeername(const fatuv_tcp_t* handle, char* ip, int* port)
{
	// ip = char[16]
	int err, namelen;
	struct sockaddr_storage peername;
	struct sockaddr_in *addr4;

	namelen = sizeof(peername);

	err = uv_tcp_getpeername(FAT2UV_HANDLE(uv_tcp_t*, handle), (struct sockaddr *)&peername, &namelen);
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

// pyobj should be in the first field
typedef struct fatuv_idle_internal_s {
	FATUV_PYOBJ_FIELDS;
	uv_idle_t handle;
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

int
fatuv_idle_init(fatuv_loop_t* loop, fatuv_idle_t* idle)
{
	return uv_idle_init((uv_loop_t*)loop, FAT2UV_HANDLE(uv_idle_t*, idle));
}

int
fatuv_idle_start(fatuv_idle_t* idle, fatuv_idle_cb cb)
{
	return uv_idle_start(FAT2UV_HANDLE(uv_idle_t*, idle), (uv_idle_cb)cb);
}

int
fatuv_idle_stop(fatuv_idle_t* idle)
{
	return uv_idle_stop(FAT2UV_HANDLE(uv_idle_t*, idle));
}

/*
 * timer
 */

typedef struct fatuv_timer_internal_s {
	FATUV_PYOBJ_FIELDS;
	uv_timer_t handle;
} fatuv_timer_internal_t;

fatuv_timer_t*
fatuv_timer_new(void)
{
	return (fatuv_timer_t*)calloc(1, sizeof(fatuv_timer_internal_t));
}

void
fatuv_timer_delete(fatuv_timer_t* timer)
{
	free(timer);
}

int
fatuv_timer_init(fatuv_loop_t* loop, fatuv_timer_t* timer)
{
	return uv_timer_init((uv_loop_t*)loop, FAT2UV_HANDLE(uv_timer_t*, timer));
}

int
fatuv_timer_start(fatuv_timer_t* timer, fatuv_timer_cb cb, uint64_t timeout, uint64_t repeat)
{
	return uv_timer_start(FAT2UV_HANDLE(uv_timer_t*, timer), (uv_timer_cb)cb, timeout, repeat);
}

int
fatuv_timer_stop(fatuv_timer_t* timer)
{
	return uv_timer_stop(FAT2UV_HANDLE(uv_timer_t*, timer));
}

int
fatuv_timer_again(fatuv_timer_t* timer)
{
	return uv_timer_again(FAT2UV_HANDLE(uv_timer_t*, timer));
}

void
fatuv_timer_set_repeat(fatuv_timer_t* timer, uint64_t repeat)
{
	uv_timer_set_repeat(FAT2UV_HANDLE(uv_timer_t*, timer), repeat);
}

uint64_t
fatuv_timer_get_repeat(const fatuv_timer_t* timer)
{
	return uv_timer_get_repeat(FAT2UV_HANDLE(uv_timer_t*, timer));
}

/*
 * signal
 */

typedef struct fatuv_signal_internal_s {
	FATUV_PYOBJ_FIELDS;
	uv_signal_t handle;
} fatuv_signal_internal_t;

fatuv_signal_t*
fatuv_signal_new(void)
{
	return (fatuv_signal_t*)calloc(1, sizeof(fatuv_signal_internal_t));
}

void
fatuv_signal_delete(fatuv_signal_t* signal)
{
	free(signal);
}

int
fatuv_signal_init(fatuv_loop_t* loop, fatuv_signal_t* signal)
{
	return uv_signal_init((uv_loop_t*)loop, FAT2UV_HANDLE(uv_signal_t*, signal));
}

int
fatuv_signal_start(fatuv_signal_t* signal, fatuv_signal_cb signal_cb, int signum)
{
	return uv_signal_start(FAT2UV_HANDLE(uv_signal_t*, signal), (uv_signal_cb)signal_cb, signum);
}

#if 0  // debian9.5 libuv1-dev package is too old
int
fatuv_signal_start_oneshot(fatuv_signal_t* signal, fatuv_signal_cb signal_cb, int signum)
{
	return uv_signal_start_oneshot(FAT2UV_HANDLE(uv_signal_t*, signal), (uv_signal_cb)signal_cb, signum);
}
#endif

int
fatuv_signal_stop(fatuv_signal_t* signal)
{
	return uv_signal_stop(FAT2UV_HANDLE(uv_signal_t*, signal));
}

/*
 * dns
 */

typedef struct fatuv_getaddrinfo_ctx_s {
	uv_getaddrinfo_t req;
	fatuv_getaddrinfo_cb callback;
} fatuv_getaddrinfo_ctx_t;

static fatuv_getaddrinfo_ctx_t*
fatuv_getaddrinfo_ctx_new(void)
{
	return (fatuv_getaddrinfo_ctx_t*)calloc(1, sizeof(fatuv_getaddrinfo_ctx_t));
}

static void
fatuv_getaddrinfo_ctx_delete(fatuv_getaddrinfo_ctx_t* ctx)
{
	free(ctx);
}

static void
fatuv_getaddrinfo_callback_internal(uv_getaddrinfo_t* req, int status, struct addrinfo* res)
{
	fatuv_getaddrinfo_ctx_t *ctx; fatuv_addrinfo_t result;

	ctx = (fatuv_getaddrinfo_ctx_t*)req;

	// TODO(kasicass): multi addrinfo
	result.family   = res->ai_family;
	result.socktype = res->ai_socktype;
	result.proto    = res->ai_protocol;

	ctx->callback(&result, status);

	fatuv_getaddrinfo_ctx_delete(ctx);
	uv_freeaddrinfo(res);
}

// TODO(kasicass): more args from py
int fatuv_getaddrinfo(fatuv_loop_t* loop, fatuv_getaddrinfo_cb getaddrinfo_cb, const char* node, const char* service)
{
	fatuv_getaddrinfo_ctx_t *ctx;
	struct addrinfo hints;

	ctx = fatuv_getaddrinfo_ctx_new();
	ctx->callback = getaddrinfo_cb;

	hints.ai_family   = PF_INET;
	hints.ai_socktype = SOCK_STREAM;	
	hints.ai_protocol = IPPROTO_TCP;
	hints.ai_flags    = 0;

	return uv_getaddrinfo(FAT2UV_HANDLE(uv_loop_t*, loop), (uv_getaddrinfo_t*)ctx,
		fatuv_getaddrinfo_callback_internal, node, service, &hints);
}

/*
 * check
 */

// pyobj should be in the first field
typedef struct fatuv_check_internal_s {
	FATUV_PYOBJ_FIELDS;
	uv_check_t handle;
} fatuv_check_internal_t;

fatuv_check_t*
fatuv_check_new(void)
{
	return (fatuv_check_t*)calloc(1, sizeof(fatuv_check_internal_t));
}

void
fatuv_check_delete(fatuv_check_t* check)
{
	free(check);
}

int
fatuv_check_init(fatuv_loop_t* loop, fatuv_check_t* check)
{
	return uv_check_init((uv_loop_t*)loop, FAT2UV_HANDLE(uv_check_t*, check));
}

int
fatuv_check_start(fatuv_check_t* check, fatuv_check_cb cb)
{
	return uv_check_start(FAT2UV_HANDLE(uv_check_t*, check), (uv_check_cb)cb);
}

int
fatuv_check_stop(fatuv_check_t* check)
{
	return uv_check_stop(FAT2UV_HANDLE(uv_check_t*, check));
}

/*
 * walk
 */

void
fatuv_walk(fatuv_loop_t* loop, fatuv_walk_cb cb, void* args)
{
	return uv_walk((uv_loop_t*)loop, (uv_walk_cb)cb, args);
}


/*
 * prepare
 */

// pyobj should be in the first field
typedef struct fatuv_prepare_internal_s {
	FATUV_PYOBJ_FIELDS;
	uv_prepare_t handle;
} fatuv_prepare_internal_t;

fatuv_prepare_t*
fatuv_prepare_new(void)
{
	return (fatuv_prepare_t*)calloc(1, sizeof(fatuv_prepare_internal_t));
}

void
fatuv_prepare_delete(fatuv_prepare_t* prepare)
{
	free(prepare);
}

int
fatuv_prepare_init(fatuv_loop_t* loop, fatuv_prepare_t* prepare)
{
	return uv_prepare_init((uv_loop_t*)loop, FAT2UV_HANDLE(uv_prepare_t*, prepare));
}

int
fatuv_prepare_start(fatuv_prepare_t* prepare, fatuv_prepare_cb cb)
{
	return uv_prepare_start(FAT2UV_HANDLE(uv_prepare_t*, prepare), (uv_prepare_cb)cb);
}

int
fatuv_prepare_stop(fatuv_prepare_t* prepare)
{
	return uv_prepare_stop(FAT2UV_HANDLE(uv_prepare_t*, prepare));
}

void
fatuv_ref(fatuv_handle_t* handle)
{
	uv_ref(FAT2UV_HANDLE(uv_handle_t*, handle));
}

void
fatuv_unref(fatuv_handle_t* handle)
{
	uv_unref(FAT2UV_HANDLE(uv_handle_t*, handle));
}

int
fatuv_has_ref(fatuv_handle_t* handle)
{
	return uv_has_ref(FAT2UV_HANDLE(uv_handle_t*, handle));
}


/*
 * tty
 */

typedef struct fatuv_tty_internal_s {
	FATUV_PYOBJ_FIELDS;
	uv_tty_t handle;
} fatuv_tty_internal_t;

fatuv_tty_t*
fatuv_tty_new(void)
{
	return (fatuv_tty_t*)calloc(1, sizeof(fatuv_tty_internal_t));
}

void fatuv_tty_delete(fatuv_tty_t* handle)
{
	free(handle);
}

int
fatuv_tty_init(fatuv_loop_t* loop, fatuv_tty_t* handle, int fd, int readable)
{
	return uv_tty_init((uv_loop_t*)loop, FAT2UV_HANDLE(uv_tty_t*, handle), fd, readable);
}

int
fatuv_tty_set_mode(fatuv_tty_t* handle, fatuv_tty_mode mode)
{
	return uv_tty_set_mode(FAT2UV_HANDLE(uv_tty_t*, handle), mode);
}

int
fatuv_tty_reset_mode(void)
{
	return uv_tty_reset_mode();
}

int
fatuv_tty_get_winsize(fatuv_tty_t* handle, int* c_with, int* c_height)
{
	return uv_tty_get_winsize(FAT2UV_HANDLE(uv_tty_t*, handle), c_with, c_height);
}

