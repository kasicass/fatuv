from _fatcore import ffi, lib
from .stream import Stream
from .. import error

uv_get_pyobj            = lib.fatuv_get_pyobj
uv_set_pyobj            = lib.fatuv_set_pyobj

uv_pipe_delete          = lib.fatuv_pipe_delete
uv_pipe_new             = lib.fatuv_pipe_new
uv_pipe_init            = lib.fatuv_pipe_init
uv_pipe_open            = lib.fatuv_pipe_open
uv_pipe_bind            = lib.fatuv_pipe_bind
uv_pipe_pending_count       = lib.fatuv_pipe_pending_count
uv_pipe_pending_type        = lib.fatuv_pipe_pending_type
uv_pipe_pending_instances   = lib.fatuv_pipe_pending_instances
uv_pipe_connect             = lib.fatuv_pipe_connect

@ffi.def_extern()
def fatuv_pipe_connect_cb(handle, status):
	ptr = uv_get_pyobj(handle)
	obj = ffi.from_handle(ptr)
	obj._call_pipe_connect_callback(status)

__all__ = ['Pipe']
class Pipe(Stream):
	def __init__(self, loop, ipc=False):
		super(Pipe, self).__init__(loop)

		handle = uv_pipe_new()
		uv_pipe_init(loop.handle, handle, int(ipc))

		self._userdata = ffi.new_handle(self)
		uv_set_pyobj(handle, self._userdata)

		self.pipe_connect_callback = None
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

	def connect(self, path, callback=None):
		if self.closing:
			raise error.HandleClosedError()
		self.pipe_connect_callback = callback or self.pipe_connect_callback
		uv_pipe_connect(self.handle, path, lib.fatuv_pipe_connect_cb)

	def _call_pipe_connect_callback(self,status):
		callback = self.pipe_connect_callback
		if callback:
			callback(self,status)
	@property
	def pending_count(self):
		if self.closing:
			return 0
		return uv_pipe_pending_count(self.handle)

	@property
	def pending_type(self):
		if self.pending_count > 0:
			return uv_pipe_pending_type(self.handle)

	# def pending_accept(self, *arguments, **keywords):
	#     if self.closing:
	#         raise error.HandleClosedError()
	#     pending_type = self.pending_type
	#     if pending_type is None:
	#         raise error.ArgumentError(message='no pending stream available')
	#     return self.accept(cls=pending_type, *arguments, **keywords)

	def pending_instances(self, amount):
		if self.closing:
			raise error.HandleClosedError()
		uv_pipe_pending_instances(self.handle, amount)

	@property
	def sockname(self):
		pass

	@property
	def peername(self):
		pass

	@property
	def family(self):
		pass
