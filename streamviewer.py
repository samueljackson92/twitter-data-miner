import re
from tweepy import StreamListener
from bcolors import bcolors
#Stream Viewer adds functionality to highlight data in a twitter stream
class StreamViewer(StreamListener):
	def highlight(self, m, color):
		return color + m + bcolors.ENDC

	def outputStream(self, status):
		try:
			text = re.sub(r"^RT", lambda m: self.highlight(m.group(0), bcolors.YELLOW), status.text) #highlight retweet
			text = re.sub(r"@\w+", lambda m: self.highlight(m.group(0), bcolors.BLUE), text) #highlight people
			text = re.sub(r"#\w+", lambda m: self.highlight(m.group(0), bcolors.RED), text) #highlight hashtags
			print text
			print "by " + bcolors.GREEN + status.author.screen_name + bcolors.ENDC + "\n"

		except UnicodeDecodeError, e:
		    # Catch any unicode errors while printing to console
		    # and just ignore them to avoid breaking application.
		    pass

	def on_status(self, status):
		self.outputStream(status)

	def on_error(self, error):
		print "HTTP Error occured with status: " + str(error)