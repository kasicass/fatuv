from _fatuv import ffi, lib
from ..stream import Stream
from .. import error

uv_get_pyobj          = lib.fatuv_get_pyobj
uv_set_pyobj          = lib.fatuv_set_pyobj

uv_pipe_new           = lib.fatuv_pipe_new
uv_pipe_delete        = lib.fatuv_pipe_delete
uv_pipe_init          = lib.fatuv_pipe_init
uv_pipe_open          = lib.fatuv_pipe_open
uv_pipe_bind       = lib.fatuv_pipe_bind


class Pipe(Stream):
    def __init__(self, loop, ipc=False):
        super(Pipe), self).__init__(loop)

        handle = uv_pipe_new()
        uv_pipe_init(loop.handle, handle, int(ipc))

        self._userdata = ffi.new_handle(self)
        uv_set_pyobj(handle, self._userdata)

        self.handle = handle

    def _dispose(self):
        handle = self.handle
        assert self.handle

        self.handle = None
        self._userdata = None

        uv_set_pyobj(handle, ffi.NULL)
        uv_pipe_delete(handle)

    def open(self, fd):
        if self.closing:
            raise error.HandleClosedError()
        code = uv_pipe_open(self.handle, fd)
        if code != error.STATUS_SUCCESS:
            raise error.UVError(code)

    def bind(self, path):
        if self.closing:
            raise error.HandleClosedError()
        code = uv_pipe_bind(self.handle, path.encode())
        if code != error.STATUS_SUCCESS:
            raise error.UVError(code)