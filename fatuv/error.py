import io

STATUS_SUCCESS = 0

class UVError(Exception):
	pass

class ThreadError(UVError):
	pass

class HandleError(UVError):
	pass

class HandleClosedError(HandleError):
	pass

class AsyncError(HandleError):
	pass

class TimerError(HandleError):
	pass

class PrepareError(HandleError):
	pass

class IdleError(HandleError):
	pass

class CheckError(HandleError):
	pass

class SignalError(HandleError):
	pass

class StreamError(HandleError):
	pass

class TCPError(StreamError):
	pass

class PipeError(StreamError):
	pass

class TTYError(StreamError):
	pass

class UDPError(HandleError):
	pass

class PollError(HandleError):
	pass

class FSError(UVError):
	pass

class FSEventError(HandleError):
	pass

class FSPollError(HandleError):
	pass

class ArgumentError(UVError, ValueError):
    """ Invalid arguments. """

class TemporaryUnavailableError(UVError, io.BlockingIOError):
    """ Resource temporary unavailable. """