all: cffi-fatuv

cffi-fatuv:
	python fatuv_builder.py
	pypy fatuv_builder.py

clean:
	rm -rf _fatuv.c *.o *.so *.pyc *.core __pycache__
