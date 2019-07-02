import sys
from _fatuv import ffi, lib
from ..handle import Handle
from .. import error

uv_get_pyobj    = lib.fatuv_get_pyobj
uv_set_pyobj    = lib.fatuv_set_pyobj

uv_fs_poll_new      = lib.fatuv_fs_poll_new
uv_fs_poll_init     = lib.fatuv_fs_poll_init
uv_fs_poll_delete   = lib.fatuv_fs_poll_delete
uv_fs_poll_start    = lib.fatuv_fs_poll_start
uv_fs_poll_stop     = lib.fatuv_fs_poll_stop


@ffi.def_extern()
def fatuv_fs_poll_callback(fs_poll_handle, status, uv_previous_stat, uv_current_stat):
	ptr = uv_get_pyobj(fs_poll_handle)
	obj = ffi.from_handle(ptr)
	obj._call_fs_poll_callback(status, uv_previous_stat, uv_current_stat)

class FSPoll(Handle):
    def __init__(self, loop, path=None, interval=5000, callback=None):
        super(FSPoll, self).__init__(loop)

        handle = uv_fs_poll_new()
        uv_fs_poll_init(loop.handle, handle)

        self.path = path
        self.interval = interval

        self._userdata = ffi.new_handle(self)
        uv_set_pyobj(handle, self._userdata)

        self.handle = handle
        self.fs_poll_callback = callback

    def _dispose(self):
        handle = self.handle
        assert handle

        self.handle = None
        self._userdata = None

        uv_set_pyobj(handle, ffi.NULL)
        uv_fs_poll_delete(handle)

    def start(self, path=None, interval=None, callback=None):
        if self.closing:
            raise error.HandleClosedError()
        
        self.path = path or self.path
        self.interval = interval or self.interval
        self.fs_poll_callback = callback or self.fs_poll_callback

        if self.path is None:
            raise error.ArgumentError('no path has been specified')

        c_path = self.path.encode()
        code = uv_fs_poll_start(self.handle, lib.fatuv_fs_poll_callback, c_path, self.interval)
        if code != error.STATUS_SUCCESS:
            raise error.UVError(code)

    def stop(self):
        if self.closing:
            return
        code = uv_fs_poll_stop(self.handle)
        if code != error.STATUS_SUCCESS:
            raise error.UVError(code)

    def _call_fs_poll_callback(self, status, uv_previous_stat, uv_current_stat):
		if self.fs_poll_callback:
			self.fs_poll_callback(self, status, uv_previous_stat, uv_current_stat)


