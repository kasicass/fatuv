import sys
from _fatuv import ffi, lib
from ..handle import Handle
from .. import error
import signal
import stream
import pipe

uv_get_pyobj    = lib.fatuv_get_pyobj
uv_set_pyobj    = lib.fatuv_set_pyobj

uv_process_new      = lib.fatuv_process_new
uv_process_delete   = lib.fatuv_process_delete
uv_spawn            = lib.fatuv_spawn
uv_process_kill     = lib.fatuv_process_kill
uv_kill             = lib.fatuv_kill

class _FD(int):
	def __repr__(self):
		return '<FileDescriptor: {}>'.format(self)

def _get_fileno(fileobj):
	try:
		return _FD(fileobj.fileno())
	except Exception:
		return None

__all__ = ['Process']

@ffi.def_extern()
def fatuv_exit_callback(process_handle, returncode, signum):
	ptr = uv_get_pyobj(process_handle)
	obj = ffi.from_handle(ptr)
	obj._call_process_callback(returncode, signum)

class CreatePipe(object):
	def __init__(self, readable=False, writable=False, ipc=False):
		self.ipc = ipc
		self.flags = lib.FATUV_CREATE_PIPE
		if readable:
			self.flags |= lib.FATUV_READABLE_PIPE
		if writable:
			self.flags |= lib.FATUV_WRITABLE_PIPE

	def __repr__(self):
		readable = bool(self.flags & lib.FATUV_READABLE_PIPE)
		writable = bool(self.flags & lib.FATUV_READABLE_PIPE)
		string = '<CreatePipe readable={}, writable={}, ipc={}>'
		return string.format(readable, writable, self.ipc)

PIPE = CreatePipe(readable=True, writable=True, ipc=True)
STDIN = _get_fileno(sys.stdin)
STDOUT = _get_fileno(sys.stdout)
STDERR = _get_fileno(sys.stderr)

def populate_stdio_container(loop, uv_stdio, file_base=None):
	fileobj = file_base
	if isinstance(file_base, stream.Stream):
		uv_stdio.data.stream = file_base.handle
		uv_stdio.flags = lib.FATUV_INHERIT_STREAM
	elif isinstance(file_base, CreatePipe):
		fileobj = pipe.Pipe(loop,ipc=file_base.ipc)
		uv_stdio.data.stream = fileobj.handle
		uv_stdio.flags = file_base.flags
	else:
		try:
			if isinstance(file_base, int):
				uv_stdio.data.fd = file_base
			else:
				uv_stdio.data.fd = file_base.fileno()
			uv_stdio.flags = lib.FATUV_INHERIT_FD
		except AttributeError:
			uv_stdio.flags = lib.FATUV_IGNORE
			if file_base is not None:
				raise error.ArgumentError()
	return fileobj

class Process(Handle):
	def __init__(self, loop, arguments, uid=None, gid=None, cwd=None, env=None, stdin=None,
			stdout=None, stderr=None, stdio=None, flags=lib.FATUV_PROCESS_WINDOWS_HIDE,callback=None):
		super(Process, self).__init__(loop)
		uv_options = ffi.new('fatuv_process_options_t*')
		c_file = ffi.new('char[]', arguments[0].encode())
		uv_options.file = c_file

		c_args_list = [ffi.new('char[]', argument.encode()) for argument in arguments]
		c_args_list.append(ffi.NULL)
		c_args = ffi.new('char*[]', c_args_list)
		uv_options.args = c_args

		stdio_count = 3
		if stdio is not None:
			stdio_count += len(stdio)
		uv_options.stdio_count = stdio_count

		c_stdio_containers = ffi.new('fatuv_stdio_container_t[]', stdio_count)
		self.stdin = populate_stdio_container(loop,c_stdio_containers[0], stdin)
		self.stdout = populate_stdio_container(loop,c_stdio_containers[1], stdout)
		self.stderr = populate_stdio_container(loop,c_stdio_containers[2], stderr)
		self.stdio = []
		if stdio is not None:
			for number in range(len(stdio)):
				c_stdio = c_stdio_containers[3 + number]
				fileobj = populate_stdio_container(loop,c_stdio, stdio[number])
				self.stdio.append(fileobj)
		uv_options.stdio = c_stdio_containers

		if cwd is not None:
			c_cwd = ffi.new('char[]', cwd.encode())
			uv_options.cwd = c_cwd

		if env is not None:
			c_env_list = [ffi.new('char[]', ('%s=%s' % item).encode())
					for item in env.items()]
			c_env_list.append(ffi.NULL)
			c_env = ffi.new('char*[]', c_env_list)
			uv_options.env = c_env

		if uid is not None:
			flags |= lib.UV_PROCESS_SETUID
		if gid is not None:
			flags |= lib.UV_PROCESS_SETGID

		uv_options.uid = uid or 0
		uv_options.gid = gid or 0

		uv_options.flags = flags
		uv_options.exit_cb = lib.fatuv_exit_callback

		self.exit_callback = callback

		handle = uv_process_new()
		code = uv_spawn(loop.handle, handle, uv_options)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

		self._userdata = ffi.new_handle(self)
		uv_set_pyobj(handle, self._userdata)
		self.handle = handle

	def _dispose(self):
		handle = self.handle
		assert handle

		self.exit_callback = None
		self.handle         = None
		self._userdata      = None

		uv_set_pyobj(handle, ffi.NULL)
		uv_process_delete(handle)

	def _call_process_callback(self, returncode, signum):
		if self.exit_callback:
			self.exit_callback(self, returncode, signum)

	def kill(self, signum=signal.SIGINT):
		if self.closing:
			raise error.HandleClosedError()
		code = uv_process_kill(self.handle, signum)
		if code != error.STATUS_SUCCESS:
			raise error.UVError(code)

	@property
	def pid(self):
		if self.closing:
			raise error.HandleClosedError()
		return lib.fatuv_process_pid(self.handle)