from tweepy import StreamListener
from textwrap import TextWrapper
import re

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

	def __init__(self, terms):
		super(MongoStreamListener, self).__init__()
		self.terms = terms

	def highlight(self, m, color):
		return color + m.group(0) + bcolors.ENDC

	def on_status(self, status):
		try:
			text = re.sub(r"^RT", lambda m: self.highlight(m, bcolors.YELLOW), status.text) #highlight retweet
			text = re.sub(r"@\w+", lambda m: self.highlight(m, bcolors.BLUE), text) #highlight people
			text = re.sub(r"#\w+", lambda m: self.highlight(m, bcolors.RED), text) #highlight hashtags
			print text
			print "by " + bcolors.GREEN + status.author.screen_name + bcolors.ENDC + "\n"
			#db.tweets.insert({"name" : status.author.screen_name})
		except UnicodeDecodeError, e:
		    # Catch any unicode errors while printing to console
		    # and just ignore them to avoid breaking application.
		    pass

	def on_error(self, error):
		print "HTTP Error occured with status: " + str(error)