#ifndef FATUV_WRAPPER_H
#define FATUV_WRAPPER_H

typedef void fatuv_loop_t;
typedef void fatuv_idle_t;

typedef void (*fatuv_idle_cb)(fatuv_idle_t* handle);

/* loop */
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

/* idle */
fatuv_idle_t* fatuv_idle_new(void);
void fatuv_idle_delete(fatuv_idle_t* idle);

int fatuv_idle_init(fatuv_loop_t* loop, fatuv_idle_t* idle);
int fatuv_idle_start(fatuv_idle_t* idle, fatuv_idle_cb cb);
int fatuv_idle_stop(fatuv_idle_t* idle);

#endif
