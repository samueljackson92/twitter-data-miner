from twython import Twython
from argparse import ArgumentParser

import json
import os

def printError(e):
	print "Error connecting to API: "
	print "\t", e

def cacheData(data):
	datastr = json.dumps(data, indent=4, separators=(',', ': '))
	metadata["last_id"] = data['search_metadata']['max_id']
	f = open("data_archive/dump" + str(metadata["last_id"]) + ".json", 'w')
	f.write(datastr)
	f.close()

	#update meta data for our search
	f = open("data_archive/meta.json", 'w')
	f.write(json.dumps(metadata))
	f.close()

def searchData():
	#authenticate onto twitter using twython
	t = Twython(app_key='a2yHDWmzXgso7PAO21TuA',
	            app_secret='WXBno2qU2TRLiJBWmF0RVN7W8rGzvtcZWA0ZES6q0ME',
	            oauth_token='480420257-l6lAeBnhOYCILqECCtDkuha2AQ3s2zRKj3ObjS4',
	            oauth_token_secret='6VYMO7JkVq3WkyrRyEDxL3BPLtcTyjtJWhmYra3fs')

	try:
		if metadata["last_id"] > 0:
			#only get results since last query
			result = t.search(q='#guncontrol sandy hook', 
				count=100, result_type='recent', since_id=metadata["last_id"])
		else:
			result = t.search(q='#guncontrol sandy hook', 
				count=100, result_type='recent')

		result_count = result["search_metadata"]["count"] 
		if(result_count > metadata["min_results"]):
			cacheData(result)
	except Exception, e:
		printError(e)

def loadData():
	path = 'data_archive/'
	data = []
	listing = os.listdir(path)
	
	for fstr in listing:
		readJSONFile("data_archive/" + fstr)
		data.append(json.loads(datastr))

	return data

def readJSONFile(path):
	#TODO - Try/except handling
	f = open(path, 'r')
	datastr = f.read()
	f.close()
	data = json.loads(datastr)
	return data

if __name__ == '__main__':
	#parse command line options
	parser = ArgumentParser(description="Grab search data from the Twitter API")
	parser.add_argument('--scan', required=False, default=False, help='Scan and collect new data from the API.')
	parser.add_argument('--load', required=False, default=False, help='Load collected data in from the file system.')
	args = parser.parse_args()

	metadata = readJSONFile("data_archive/meta.json")

	if args.scan:
		searchData()
	elif args.load:
		loadData()
