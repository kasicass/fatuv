from _fatuv import ffi, lib
from .stream import Stream
from .. import error

uv_get_pyobj          = lib.fatuv_get_pyobj
uv_set_pyobj          = lib.fatuv_set_pyobj

uv_tty_new            = lib.fatuv_tty_new
uv_tty_delete         = lib.fatuv_tty_delete
uv_tty_init           = lib.fatuv_tty_init
uv_tty_set_mode       = lib.fatuv_tty_set_mode
uv_tty_reset_mode     = lib.fatuv_tty_reset_mode
uv_tty_get_winsize    = lib.fatuv_tty_get_winsize

__all__ = ['TTY']

UV_TTY_MODE_NORMAL  = lib.FATUV_TTY_MODE_NORMAL
UV_TTY_MODE_RAW     = lib.FATUV_TTY_MODE_RAW
UV_TTY_MODE_IO   = lib.FATUV_TTY_MODE_IO

def reset_mode():
        code = uv_tty_reset_mode()
        if code != error.STATUS_SUCCESS:
            raise error.UVError(code)

class TTY(Stream):
    def __init__(self, loop, fd, readable=False):
        super(TTY, self).__init__(loop)

        handle = uv_tty_new()
        uv_tty_init(loop.handle, handle, fd, int(readable))

        self._userdata = ffi.new_handle(self)
        uv_set_pyobj(handle, self._userdata)

        self.handle = handle

    def _dispose(self):
        handle = self.handle
        assert self.handle

        self.handle = None
        self._userdata = None

        uv_set_pyobj(handle, ffi.NULL)
        uv_tty_delete(handle)

    def set_mode(self, mode=UV_TTY_MODE_NORMAL):
        if self.closing:
            raise error.HandleClosedError()
        code = uv_tty_set_mode(self.handle, mode)
        if code != error.STATUS_SUCCESS:
            raise error.UVError(code)

    @property
    def console_size(self):
        if self.closing:
            return (0,0)
        c_with, c_height = ffi.new('int*'), ffi.new('int*')
        code = uv_tty_get_winsize(self.handle, c_with, c_height)
        if code != error.STATUS_SUCCESS:
            raise error.UVError(code)
        return (c_with[0], c_height[0])