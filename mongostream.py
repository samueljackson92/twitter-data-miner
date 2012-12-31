from tweepy import Stream


class MongoStream(Stream):
	def _data(self, data):
		super(MongoStream, self)._data(data)
