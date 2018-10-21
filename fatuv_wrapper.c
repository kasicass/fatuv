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

