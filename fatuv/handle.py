from __future__ import print_function
from _fatuv import ffi, lib
from .error import HandleError
import error
from .internal import get_strerror
from loop import Loop

uv_get_pyobj  = lib.fatuv_get_pyobj
uv_set_pyobj  = lib.fatuv_set_pyobj

uv_close      = lib.fatuv_close
uv_is_active  = lib.fatuv_is_active
uv_is_closing = lib.fatuv_is_closing
uv_fileno     = lib.fatuv_fileno
uv_ref		  = lib.fatuv_ref
uv_unref	  = lib.fatuv_unref
uv_has_ref	  = lib.fatuv_has_ref

__all__ = ['Handle',]

@ffi.def_extern()
def fatuv_close_callback(handle):
	ptr = uv_get_pyobj(handle)
	# print('fatuv_close_callback')
	obj = ffi.from_handle(ptr)
	# print('fatuv_close_callback2')
	obj._call_close_callback()

class Handle(object):
	def __init__(self, loop):
		self.loop           = loop or Loop.default_loop()
		self.handle         = None       # initialize by derived class
		self.close_callback = None
		self.closing = False

	def close(self, callback=None):
		assert self.handle
		if self.closing:
			return
		self.closing = True
		self.close_callback = callback
		self.set_pending()
		uv_close(self.handle, lib.fatuv_close_callback)

	def set_pending(self):
		self.loop.set_pending(self)

	def clear_pending(self):
		self.loop.clear_pending(self)

	def _call_close_callback(self):
		callback = self.close_callback
		self.clear_pending()
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

	def reference(self):
		if self.closing:
			raise error.HandleClosedError()
		uv_ref(self.handle)

	def dereference(self):
		if self.closing:
			raise error.HandleClosedError()
		uv_unref(self.handle)

	@property
	def referenced(self):
		if self.closed:
			return False
		return bool(uv_has_ref(self.handle))
