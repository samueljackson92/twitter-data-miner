import tweepy
import json
from getpass import getpass

from argparse import ArgumentParser
from pymongo import MongoClient

from mongostreamlistener import MongoStreamListener

def loadFile(path):
	try:
		f = open(path, 'r')
		data = f.read()
		f.close()
	except Exception, e:
		print "Could not read file: %s" % path
		print "Error: %s" % e
		exit(-1)

	return data

def loadJSONFile(path):
	try:
		data = json.loads(loadFile(path))
		return data
	except Exception, e:
		print "Could not read JSON file: %s" % path
		print "Error: %s" % e
		exit(-1)



_config = loadJSONFile(".config.json")

twData = _config["twitter_auth_data"]
mongoData = _config["mongo_config"]

#Use OAuth to connect to Twitter
auth = tweepy.OAuthHandler(twData["consumer_key"], twData["consumer_secret"])
auth.set_access_token(twData["access_token"], twData["access_token_secret"])

#Create connection to mongodb
connection = MongoClient(mongoData["host"], mongoData["port"])
db = connection.twitterdb


if __name__ == "__main__":
		#parse command line options
	parser = ArgumentParser(description="Grabs data from the Twitter API and stores it in a MongoDB Database.")
	
	parser.add_argument('--terms', 
		type=str, nargs='+', required=False, help='Provide a list of search terms used to collect data from the API.')

	parser.add_argument('--file', type=str, nargs=1, required=False, help='Provide a path to a JSON file of terms to collect data from the API.')

	args = parser.parse_args()
	terms = []

	if args.file:	#load a list of terms from a file
		data = loadFile(args.file[0])
		terms = [term for term in data.strip().split('\n')]
	elif args.terms:	#read in a list of terms from the commandline
		terms = args.terms

	#connect to twitter stream and collect some tweets!
	if terms:
		print "\n\nEnter [x] to quit the stream..."
		print "Connecting to stream...\n"
		streamer = tweepy.Stream(auth=auth, listener=MongoStreamListener(terms), timeout=60)
		streamer.filter(None,terms, async=True)

		while True:
			opt = getpass()
			if opt == 'x':
				break

		print "Quitting strean..."
		streamer.disconnect()
	else:
		parser.print_usage()

