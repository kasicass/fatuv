from _fatuv import ffi, lib
from .error import HandleError
from .internal import get_strerror

uv_close      = lib.fatuv_close
uv_is_active  = lib.fatuv_is_active
uv_is_closing = lib.fatuv_is_closing
uv_fileno     = lib.fatuv_fileno

__all__ = ['Handle',]

@ffi.def_extern()
def fatuv_close_callback(handle):
	handle = Handle.closing_instances[handle]
	handle._call_close_callback()

class Handle(object):
	closing_instances = {}

	def __init__(self, loop):
		self.loop           = loop
		self.handle         = None       # initialize by derived class
		self.close_callback = None

	def close(self, callback=None):
		assert self.handle
		self.close_callback = callback
		Handle.closing_instances[self.handle] = self
		uv_close(self.handle, lib.fatuv_close_callback)

	def _call_close_callback(self):
		callback = self.close_callback
		if callback:
			self.close_callback = None
			callback(self)

		self._dispose()

	def _dispose(self):
		raise NotImplementedError

	@property
	def active(self):
		assert self.handle
		return bool(uv_is_active(self.handle))

	@property
	def closed(self):
		assert self.handle
		return bool(uv_is_closing(self.handle))

	def fileno(self):
		assert self.handle
		ptr = ffi.new('int*')
		err = uv_fileno(self.handle, ptr)
		if err < 0:
			raise HandleError((err, get_strerror(err)))
		return ptr[0]

