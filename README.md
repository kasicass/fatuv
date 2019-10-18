# fatuv

## INTRODUCTION

* a cffi-based libuv wrapper for python/pypy
* interface inspired by [pyuv][1]
* benchmark inspired by [uvloop][2]


## BUILD

### Debian 9.5

```
aptitude install make gcc
aptitude install python-dev python3-dev pypy pypy-dev
aptitude install libtoolize

$ python build_libuv.py clone
$ python build_libuv.py build
```

### OpenBSD 6.4

```
# pkg_add -v pypy gmake automake-1.16.1 autoconf-2.69p2 libtool

$ vim ~/.profile
AUTOMAKE_VERSION="1.16"
AUTOCONF_VERSION="2.69"

```

### Python & PyPy

```
# python -m pip install cffi
# pypy -m pip install pycparser

$ make py2
$ python tests/test_timer.py
```


## SCHEDULE

handles (test pass)
- [x] CHECK
- [x] ASYNC
- [x] IDLE
- [x] PIPE
- [x] POLL
- [x] PREPARE
- [x] PROCESS
- [x] SIGNAL
- [x] STREAM
- [x] TCP
- [x] TIMER
- [x] TTY
- [x] UDP
- [x] FS_EVENT
- [x] FS_POLL

requests (test pass)
- [x] CONNECT
- [x] WRITE
- [x] SHUTDOWN
- [ ] FS
- [ ] WORK
- [x] GETADDRINFO
- [ ] GETNAMEINFO
- [x] UDP_SEND
- [x] DNS


[1]: https://github.com/saghul/pyuv/
[2]: https://github.com/MagicStack/uvloop

