from twython import Twython
from argparse import ArgumentParser

import json
import os

def printError(e):
	print "An error occured: "
	print "\t", e

def writeJSONFile(path, data):
	try:
		f = open(path, 'w')
		datastr = json.dumps(data, indent=4, separators=(',', ': '))
		f.write(datastr)
		f.close()
	except IOError, e:
		raise e

def cacheData(data):
	metadata["last_id"] = data['search_metadata']['max_id']
	metadata["total"] += data['search_metadata']['count']
	directory = "data_archive/"

	#cache the collected data
	print "Writing collected data..."
	writeJSONFile(directory + "dump" + str(metadata["last_id"]) + ".json", data)

	#update meta data for our search
	print "Writing meta data..."
	writeJSONFile(directory + "meta.json", metadata)

	print "Data capture successful!"

def searchData(terms):
	#authenticate onto twitter using twython
	print "Connecting to Twitter API..."
	t = Twython(app_key='a2yHDWmzXgso7PAO21TuA',
	            app_secret='WXBno2qU2TRLiJBWmF0RVN7W8rGzvtcZWA0ZES6q0ME',
	            oauth_token='480420257-l6lAeBnhOYCILqECCtDkuha2AQ3s2zRKj3ObjS4',
	            oauth_token_secret='6VYMO7JkVq3WkyrRyEDxL3BPLtcTyjtJWhmYra3fs')

	#convert list of terms into search string
	termsstr = ' '.join(terms)

	try:
		print "Searching for data..."
		if metadata["last_id"] > 0:
			#only get results since last query
			result = t.search(q=termsstr, 
				count=100, result_type='recent', since_id=metadata["last_id"])
		else:
			result = t.search(q=termsstr, 
				count=100, result_type='recent')
		
		result_count = result["search_metadata"]["count"] 
		if(result_count > metadata["min_results"]):
			print "Successfully found more than " + str(metadata["min_results"])
			print "Caching data..."
			cacheData(result)
		else:
			print "Failed to find more than the " + str(metadata["min_results"])

	except Exception, e:
		printError(e)

def readJSONFile(path):
	try:
		f = open(path, 'r')
		datastr = f.read()
		f.close()
		data = json.loads(datastr)
	except Exception, e:
		raise e
	return data

def newDataScan(directory):
	os.makedirs(directory)
	meta = {}
	meta["last_id"] = 0
	meta["min_results"] = 50
	meta["total"] = 0
	return meta

if __name__ == '__main__':
	#parse command line options
	parser = ArgumentParser(description="Grab search data from the Twitter API")
	
	parser.add_argument('directory', metavar='Directory', 
		action='store', help='The directory of to store collected data in. If none exists it will be initialised.')
	
	parser.add_argument('terms', metavar='Terms', 
		type=str, nargs='+', help='List of search terms used to collect data from the API.')

	parser.add_argument('-m', '--min', action='store', 
		help='Minimum number of new tweets to find if data collection is to be successful. Default is 50.')
	
	args = parser.parse_args()

	if not os.path.exists(args.directory):
		print "Making new data cache..."
		metadata = newDataScan(args.directory)
	else:
		print "Loading meta data..."
		try:
			metadata = readJSONFile(args.directory + "/meta.json")
		except IOError as e:
			print "No meta file exists!"

	if args.min:
		metadata["min_results"] = args.min

	print "Beginning search..."
	searchData(args.terms)
