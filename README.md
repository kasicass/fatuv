# fatuv

## INTRODUCTION

* a cffi-based libuv wrapper for python/pypy
* interface inspired by [pyuv][1]
* benchmark inspired by [uvloop][2]

## BUILD

```
# python -m pip install cffi
# pypy -m pip install cffi
```

```
$ make
$ python uv-hello.py 
$ pypy uv-hello.py
```

[1]: https://github.com/saghul/pyuv/
[2]: https://github.com/MagicStack/uvloop

