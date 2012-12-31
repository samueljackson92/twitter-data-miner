
from textwrap import TextWrapper
from bcolors import bcolors
from streamviewer import StreamViewer

class MongoStreamListener(StreamViewer):
	status_wrapper = TextWrapper(width=60, 
		initial_indent='    ', subsequent_indent='    ')

	settings = {}
	status_count = 0

	def __init__(self, dbhandle, limit=0, listen=False, name=''):
		super(MongoStreamListener, self).__init__()
		self.settings["limit"] = limit
		self.settings["listen"] = listen
		self.db = dbhandle
		self.name = name

	def getTweetsCaptured():
		return status_count

	def capture(self, status):

		#insert tweet into mongo db
		self.db.tweets[self.name].insert(
			{
				"tweet_id" : status.id,
				"user" : {
					"username" : status.author.screen_name,
					"name" : status.author.name,
				},
				"text" : status.text,
				"time" : status.created_at
			})

		#Output the number of tweets collected
		if(self.status_count % 10) == 0:
			print self.highlight(str(self.status_count) + " tweets collected.", bcolors.PURPLE) + "\n"

	def on_status(self, status):
		self.outputStream(status)

		self.status_count += 1
		if not self.settings["listen"]:
			self.capture(status)

		if self.settings["limit"] > 0 and self.status_count >= self.settings["limit"]:
			print "Collected required number of tweets! Disconnecting..."
			print "Enter [x] to quit."

			#Exit thread
			return False
