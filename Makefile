all: cffi-fatuv

cffi-fatuv:
	pypy fatuv_builder.py

clean:
	rm -rf _fatuv.c *.o *.so *.pyc
