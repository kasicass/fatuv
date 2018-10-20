import fatuv

loop = fatuv.uv_default_loop()

print 'Now quitting.'
fatuv.uv_run(loop, fatuv.UV_RUN_DEFAULT)

