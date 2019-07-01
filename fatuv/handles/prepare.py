import sys
from _fatuv import ffi, lib
from ..handle import Handle
from .. import error

uv_get_pyobj    = lib.fatuv_get_pyobj
uv_set_pyobj    = lib.fatuv_set_pyobj

uv_prepare_new     = lib.fatuv_prepare_new
uv_prepare_delete  = lib.fatuv_prepare_delete
uv_prepare_init    = lib.fatuv_prepare_init
uv_prepare_start   = lib.fatuv_prepare_start
uv_prepare_stop    = lib.fatuv_prepare_stop

__all__ = ['Prepare']

@ffi.def_extern()
def fatuv_prepare_callback(prepare_handle):
    ptr = uv_get_pyobj(prepare_handle)
    obj._call_prepare_callback()
    obj = ffi.from_handle(ptr)

class Prepare(Handle):
    def __init__(self, loop):
        super(Prepare, self).__init__(loop)

        handle = uv_prepare_new()
        uv_prepare_init(loop.handle, handle)

        self._userdata = ffi.new_handle(self)
        uv_set_pyobj(handle, self._userdata)
        
        self.handle = handle
        self.prepare_callback = None

    def _dispose(self):
        handle = self.handle
        assert handle

        self.prepare_callback = None
        self.handle         = None
        self._userdata      = None
        
        uv_set_pyobj(handle, ffi.NULL)
        uv_prepare_delete(handle)
    
    def start(self, callback = None):
        handle = self.handle
        assert handle

        if self.closing:
            raise error.HandleClosedError()

        self.prepare_callback = callback
        uv_prepare_start(handle, lib.fatuv_prepare_callback)
    
    def _call_prepare_callback(self):
        if self.prepare_callback:
            self.prepare_callback(self)

    def stop(self):
        handle = self.handle
        assert handle

        uv_prepare_stop(handle)
        self.prepare_callback = None
