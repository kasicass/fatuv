import sys
sys.path.append('.')
from _fatcore import ffi, lib
import json
import bson
mongo_new = lib.mongo_new
mongo_find = lib.mongo_find
mongo_find_one = lib.mongo_find_one

@ffi.def_extern()
def mongo_find_callback(data, len, userdata):
	data2 = ffi.unpack(data, len)
	ret = []
	for d in data2:
		ret.append(ffi.unpack(d.base, d.len))
	obj = ffi.from_handle(userdata)
	obj.find_callback(ret)

class MongoFindRequest():
	def __init__(self, mongoclient, ccol, cbuf, callback):
		self._userdata = ffi.new_handle(self)
		self.callback = callback
		self.mongoclient = mongoclient
		mongo_find(mongoclient._mongo, ccol, cbuf, lib.mongo_find_callback, self._userdata)
		self.mongoclient.set_pending(self)

	def find_callback(self, ret):
		print()
		callback = self.callback or None
		self.mongoclient.clear_pending(self)
		if callback:
			callback(ret)

class MongoClient():
	def __init__(self, uri):
		userdata = ffi.new_handle(self)
		self._userdata = userdata
		uribuf = ffi.new('char[]', uri)
		self._mongo = mongo_new(userdata, uribuf)
		self.callback = None
		self.pending = set()

	def set_pending(self, structure):
		self.pending.add(structure)

	def clear_pending(self, structure):
		try:
			self.pending.remove(structure)
		except KeyError:
			pass

	def find(self, collection, query, callback):
		cbuf = ffi.new('char[]', json.dumps(query))
		ccol = ffi.new('char[]', collection)
		return MongoFindRequest(self, ccol, cbuf, callback)

	def findOne(self, collection, query, callback):
		cbuf = ffi.new('char[]', json.dumps(query))
		self.callback = callback
		ccol = ffi.new('char[]', collection)
		mongo_find_one(self._mongo, ccol, cbuf, lib.mongo_find_callback)

def main():
	uri = "mongodb://commondb:commondb@192.168.11.247:30000/?authSource=tw2_commondb&authMechanism=SCRAM-SHA-1"
	m = MongoClient(uri)
	import os
	print("os.getpid(),%s",os.getpid())
	def callback(result):
		for r in result:
			print(r)
	m.find('testcollection', {'hello':'world2'}, callback)
	# m.findOne('testcollection', {'hello':'world4'}, callback)
	
	lib.uv_poll()
	
	print(1231221)

if __name__ == "__main__":
	main()