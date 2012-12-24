import tweepy
from getpass import getpass
from argparse import ArgumentParser
from pymongo import MongoClient

#Local dependencies
from fileio import FileIO
from mongostream import MongoStream
from mongostreamlistener import MongoStreamListener


class TwDataMiner(object):
	def __init__(self):
		#load configuration settings
		_config = FileIO().loadJSONFile("config.json")

		self.twData = _config["twitter_auth_data"]
		self.mongoData = _config["mongo_config"]

		#parse command line options
		self.parser = ArgumentParser(
			description="Grabs data from the Twitter API and stores it in a MongoDB Database.")
		

		self.parser.add_argument('-t', '--terms', 
			type=str, nargs='+', required=False, 
			help='Provide a list of search terms used to collect data from the API.')

		self.parser.add_argument('-f', '--file', 
			type=str, nargs=1, required=False, 
			help='Provide a path to a JSON file of terms to collect data from the API.')

		self.parser.add_argument('-c', '--count', 
			type=int, required=False,
			help="Collect the specified number of tweets.")

		self.parser.add_argument('-l', '--listen', 
			action='store_true', required=False, 
			help="Just open the stream and listen. Don't connect to database.")

		self.args = self.parser.parse_args()

	def twitterConnect(self):
		#Use OAuth to connect to Twitter
		self.auth = tweepy.OAuthHandler(self.twData["consumer_key"], self.twData["consumer_secret"])
		self.auth.set_access_token(self.twData["access_token"], self.twData["access_token_secret"])

	def mongodbConnect(self):
		#Create connection to mongodb
		connection = MongoClient(self.mongoData["host"], self.mongoData["port"])
		self.db = connection.twitterdb

	def connect(self):
		self.twitterConnect()
		self.mongodbConnect()

	def startStreaming(self):
		if self.db and self.auth:
			terms = []

			if self.args.file:	#load a list of terms from a file
				data = FileIO().loadFile(self.args.file[0])
				terms = [term for term in data.strip().split('\n')]
			elif self.args.terms:	#read in a list of terms from the commandline
				terms = self.args.terms

			#connect to twitter stream and collect some tweets!
			if terms:
				print "\n\nEnter [x] to quit the stream..."
				print "Connecting to stream..."

				listener = MongoStreamListener(self.db, listen=self.args.listen, limit=self.args.count)
				streamer = MongoStream(auth=self.auth, listener=listener, timeout=60)

				print "Connected. Filtering tweets...\n"
				streamer.filter(None,terms, async=True)

				while True:
					opt = getpass('')
					if opt == 'x':
						break

				print "Quitting..."
				streamer.disconnect()
			else:
				self.parser.print_usage()


if __name__ == "__main__":
	dm = TwDataMiner()
	dm.connect()
	dm.startStreaming()
