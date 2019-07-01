import sys
from _fatuv import ffi, lib
from ..handle import Handle
from .. import error

uv_get_pyobj    = lib.fatuv_get_pyobj
uv_set_pyobj    = lib.fatuv_set_pyobj

uv_check_new     = lib.fatuv_check_new
uv_check_delete  = lib.fatuv_check_delete
uv_check_init    = lib.fatuv_check_init
uv_check_start   = lib.fatuv_check_start
uv_check_stop    = lib.fatuv_check_stop

__all__ = ['Check']

@ffi.def_extern()
def fatuv_check_callback(check_handle):
    ptr = uv_get_pyobj(check_handle)
    obj = ffi.from_handle(ptr)
    obj._call_check_callback()

class Check(Handle):
    def __init__(self, loop):
        super(Check, self).__init__(loop)

        handle = uv_check_new()
        uv_check_init(loop.handle, handle)

        self._userdata = ffi.new_handle(self)
        uv_set_pyobj(handle, self._userdata)
        
        self.handle = handle
        self.check_callback = None

    def _dispose(self):
        handle = self.handle
        assert handle

        self.check_callback = None
        self.handle         = None
        self._userdata      = None
        
        uv_set_pyobj(handle, ffi.NULL)
        uv_check_delete(handle)
    
    def start(self, callback = None):
        handle = self.handle
        assert handle

        if self.closing:
            raise error.HandleClosedError()

        self.check_callback = callback
        uv_check_start(handle, lib.fatuv_check_callback)
    
    def _call_check_callback(self):
        if self.check_callback:
            self.check_callback(self)

    def stop(self):
        handle = self.handle
        assert handle

        uv_check_stop(handle)
        self.check_callback = None
