from tweepy import StreamListener
from textwrap import TextWrapper

class bcolors:
	GREEN = '\033[92m'
	ENDC = '\033[0m'


class MongoStreamListener(StreamListener):
	status_wrapper = TextWrapper(width=60, 
		initial_indent='    ', subsequent_indent='    ')

	def on_status(self, status):
		try:
			print status.text
			print "by " + bcolors.GREEN + status.author.screen_name + bcolors.ENDC + "\n"
			#db.tweets.insert({"name" : status.author.screen_name})
		except Exception, e:
		    # Catch any unicode errors while printing to console
		    # and just ignore them to avoid breaking application.
		    pass

	def on_error(self, error):
		print "HTTP Error occured with status: " + str(error)