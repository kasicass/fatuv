import sys
from _fatcore import ffi, lib
from ..handle import Handle
from .. import error

uv_get_pyobj    = lib.fatuv_get_pyobj
uv_set_pyobj    = lib.fatuv_set_pyobj

uv_fs_event_new      = lib.fatuv_fs_event_new
uv_fs_event_init     = lib.fatuv_fs_event_init
uv_fs_event_delete   = lib.fatuv_fs_event_delete
uv_fs_event_start    = lib.fatuv_fs_event_start
uv_fs_event_stop     = lib.fatuv_fs_event_stop

UV_FS_EVENTS_RENAME     = lib.FATUV_FS_EVENTS_RENAME
UV_FS_EVENTS_CHANGE     = lib.FATUV_FS_EVENTS_CHANGE
UV_FS_EVENTS_MODE_IO    = lib.FATUV_FS_EVENTS_MODE_IO

UV_FS_EVENT_FLAGS_WATCH_ENTRY   = lib.FATUV_FS_EVENT_FLAGS_WATCH_ENTRY
UV_FS_EVENT_FLAGS_STAT          = lib.FATUV_FS_EVENT_FLAGS_STAT
UV_FS_EVENT_FLAGS_RECURSIVE     = lib.FATUV_FS_EVENT_FLAGS_RECURSIVE


@ffi.def_extern()
def fatuv_fs_event_callback(fs_event_handle, c_filename, events, status):
	ptr = uv_get_pyobj(fs_event_handle)
	obj = ffi.from_handle(ptr)
	filename = ffi.string(c_filename).decode()
	obj._call_fs_event_callback(filename, events, status)

class FSEvent(Handle):
	def __init__(self, loop, path=None, flags=0, callback=None):
		super(FSEvent, self).__init__(loop)

		handle = uv_fs_event_new()
		uv_fs_event_init(loop.handle, handle)

		self.path = path
		self.flags = flags

		self._userdata = ffi.new_handle(self)
		uv_set_pyobj(handle, self._userdata)

		self.handle = handle
		self.fs_event_callback = callback

	def _dispose(self):
		handle = self.handle
		assert handle

		self.handle = None
		self._userdata = None

		uv_set_pyobj(handle, ffi.NULL)
		uv_fs_event_delete(handle)

	def start(self, path=None, flags=None, callback=None):
		if self.closing:
			raise error.HandleClosedError()

		self.path = path or self.path
		self.flags = flags or self.flags
		self.fs_event_callback = callback or self.fs_event_callback

		if self.path is None:
			raise error.ArgumentError('no path has been specified')

		c_path = self.path.encode()
		code = uv_fs_event_start(self.handle, lib.fatuv_fs_event_callback, c_path, self.flags)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def stop(self):
		if self.closing:
			return
		code = uv_fs_event_stop(self.handle)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	def _call_fs_event_callback(self, filename, events, status):
		if self.fs_event_callback:
			self.fs_event_callback(self, filename, events, status)
