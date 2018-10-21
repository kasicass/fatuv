# fatuv

## INTRODUCTION

* a cffi-based libuv wrapper for python/pypy
* interface inspired by [pyuv][1]
* benchmark inspired by [uvloop][2]

## BUILD

```
# python -m pip install cffi
# pypy -m pip install pycparser

$ make
$ python uv-hello.py 
$ pypy uv-hello.py
```

## Debian 9.5

```
aptitude install make gcc libuv1-dev pypy pypy-dev
```

## OpenBSD 6.3

```
pkg_add -v pypy
```


[1]: https://github.com/saghul/pyuv/
[2]: https://github.com/MagicStack/uvloop

