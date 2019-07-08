# fatuv

## INTRODUCTION

* a cffi-based libuv wrapper for python/pypy
* interface inspired by [pyuv][1]
* benchmark inspired by [uvloop][2]


## BUILD

### DEPENDS ON libuv SOURCES

#### Debian 9.5

```
aptitude install make gcc libuv1-dev
aptitude install python-dev python3-dev pypy pypy-dev
```

#### OpenBSD 6.4

```
# pkg_add -v pypy gmake automake-1.16.1 autoconf-2.69p2 libtool

$ vim ~/.profile
AUTOMAKE_VERSION="1.16"
AUTOCONF_VERSION="2.69"

$ python build_libuv.py clone
$ python build_livuv.py build
```


### DEPENDS ON SYSTEM PACKAGES

```
# python -m pip install cffi
# pypy -m pip install pycparser

$ make
$ python examples/08-timer.py
$ pypy examples/08-timer.py
```

#### Debian 9.5

```
aptitude install make gcc libuv1-dev
aptitude install python-dev python3-dev pypy pypy-dev
```

#### OpenBSD 6.4

```
pkg_add -v pypy libuv gmake
```


[1]: https://github.com/saghul/pyuv/
[2]: https://github.com/MagicStack/uvloop

SCHEDULE

handles (test pass)
- [x] CHECK
- [x] ASYNC
- [ ] FILE
- [x] IDLE
- [ ] PIPE
- [x] POLL
- [x] PREPARE
- [ ] PROCESS
- [x] SIGNAL
- [x] STREAM
- [x] TCP
- [x] TIMER
- [x] TTY
- [ ] UDP
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
- [ ] UDP_SEND
