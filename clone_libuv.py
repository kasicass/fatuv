import os
import os.path
import subprocess

DEPS_PATH='./'
LIBUV_PATH = os.path.join(DEPS_PATH, 'libuv')
LIBUV_REPO = 'https://github.com/libuv/libuv.git'
LIBUV_BRANCH = 'v1.x'
LIBUV_TAG = 'v1.30.1'

def clone_libuv():
	print('cloning libuv...')
	cmd = ['git', 'clone', '-b', LIBUV_BRANCH, LIBUV_REPO, LIBUV_PATH]
	subprocess.check_call(cmd)
	subprocess.check_call(['git', 'checkout', LIBUV_TAG], cwd=LIBUV_PATH)

def main():
	clone_libuv()

if __name__ == "__main__":
	main()
