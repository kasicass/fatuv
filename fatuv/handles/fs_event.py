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

        
        


