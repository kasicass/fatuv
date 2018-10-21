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
 * idle
 */

fatuv_idle_t*
fatuv_idle_new(void)
{
	return (fatuv_idle_t*)malloc(sizeof(uv_idle_t));
}

void
fatuv_idle_delete(fatuv_idle_t* idle)
{
	free(idle);
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

