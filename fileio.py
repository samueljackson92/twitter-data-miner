import json

class FileIO(object):
	def loadFile(self,path):
		try:
			f = open(path, 'r')
			data = f.read()
			f.close()
		except Exception, e:
			print "Could not read file: %s" % path
			print "Error: %s" % e
			exit(-1)

		return data

	def loadJSONFile(self,path):
		try:
			data = json.loads(self.loadFile(path))
			return data
		except Exception, e:
			print "Could not read JSON file: %s" % path
			print "Error: %s" % e
			exit(-1)
