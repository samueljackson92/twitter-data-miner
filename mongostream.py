from tweepy import Stream


class MongoStream(Stream):
	#used to disconnect when listener has heard enough
	get_status = False
	def _data(self, data):
		if self.listener.isFinished():
			self.disconnect()
		else:
			super(MongoStream, self)._data(data)
