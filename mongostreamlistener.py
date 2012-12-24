from tweepy import StreamListener
from textwrap import TextWrapper
import re
import sys

class bcolors:
	PURPLE = '\033[95m'
	GREEN = '\033[92m'
	BLUE = '\033[94m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'


class MongoStreamListener(StreamListener):
	status_wrapper = TextWrapper(width=60, 
		initial_indent='    ', subsequent_indent='    ')

	settings = {}
	status_count = 0
	finished = False

	def __init__(self, dbhandle, limit=None, listen=False):
		super(MongoStreamListener, self).__init__()
		self.settings["limit"] = limit
		self.settings["listen"] = listen
		self.db = dbhandle

	def highlight(self, m, color):
		return color + m.group(0) + bcolors.ENDC

	def outputStream(self, status):
		try:
			text = re.sub(r"^RT", lambda m: self.highlight(m, bcolors.YELLOW), status.text) #highlight retweet
			text = re.sub(r"@\w+", lambda m: self.highlight(m, bcolors.BLUE), text) #highlight people
			text = re.sub(r"#\w+", lambda m: self.highlight(m, bcolors.RED), text) #highlight hashtags
			print text
			print "by " + bcolors.GREEN + status.author.screen_name + bcolors.ENDC + "\n"

		except UnicodeDecodeError, e:
		    # Catch any unicode errors while printing to console
		    # and just ignore them to avoid breaking application.
		    pass

	def capture(self, status):
		if(self.status_count % 100) == 0:
			print bcolors.PURPLE + str(self.status_count) + " tweets collected." + bcolors.ENDC
		#db.tweets.insert({"name" : status.author.screen_name})

	def isFinished(self):
		return self.finished


	############################################
	#Stream Callbacks
	############################################
	def on_status(self, status):
		self.outputStream(status)

		self.status_count += 1
		if not self.settings["listen"]:
			self.capture(status)

		if self.status_count >= self.settings["limit"]:
			print "Collected required number of tweets! Disconnecting..."
			print "Enter [x] to quit."
			self.finished = True


	def on_error(self, error):
		print "HTTP Error occured with status: " + str(error)