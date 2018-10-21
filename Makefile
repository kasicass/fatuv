all: cffi-fatuv

cffi-fatuv:
	cd src && python fatuv_builder.py
	cd src && pypy fatuv_builder.py
	mv src/*.so ./

clean:
	cd src && rm -rf _fatuv.c *.o *.so
	rm -rf *.so *.pyc *.core __pycache__
	rm -rf fatuv/*.pyc

