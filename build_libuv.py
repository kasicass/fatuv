import os
import os.path
import subprocess
import sys

DEPS_PATH='./'
LIBUV_PATH = os.path.join(DEPS_PATH, 'libuv')
LIBUV_REPO = 'https://github.com/libuv/libuv.git'
LIBUV_BRANCH = 'v1.x'
LIBUV_TAG = 'v1.9.0'

def clone_libuv():
    print('cloning libuv...')
    cmd = ['git', 'clone', '-b', LIBUV_BRANCH, LIBUV_REPO, LIBUV_PATH]
    subprocess.check_call(cmd)
    subprocess.check_call(['git', 'checkout', LIBUV_TAG], cwd=LIBUV_PATH)

def build_libuv():
	print('building libuv...')
	env=dict(os.environ)
	subprocess.check_call(['sh', 'autogen.sh'], cwd=LIBUV_PATH, env=env)
	subprocess.check_call(['./configure'], cwd=LIBUV_PATH, env=env)
	subprocess.check_call(['make'], cwd=LIBUV_PATH, env=env)

def clean_libuv():
	print('cleaning libuv...')
	subprocess.check_call(['make', 'clean'], cwd=LIBUV_PATH)
	subprocess.check_call(['make', 'distclean'], cwd=LIBUV_PATH)

def clean_build():
	print('cleaning build...')
	shutil.rmtree(DEPS_PATH)


def print_help():
	print("""Usage:
		python op_libuv.py clone
		python op_libuv.py build
		python op_libuv.py clean
		python op_libuv.py cleanbuild
	""")

def main():
	if len(sys.argv) != 2:
		print_help()
		return
	if sys.argv[1] == 'clone':
		clone_libuv()
	elif sys.argv[1] == 'build':
		build_libuv()
	elif sys.argv[1] == 'clean':
		clean_libuv()
	elif sys.argv[1] == 'cleanbuild':
		clean_build()
	else:
		print_help()

if __name__ == "__main__":
	main()
