twitter-data-miner
==================

Python application to collect a large sample of tweets from twitter which can then be used for data mining. Uses JSON encoding as the primary data format and stores the results in a MongoDB database.

Configuration
--------------

This application loads the settings required to run from a file called config.json stored in the parent directory. The settings in this file can be configured to match your requirements.

```json

{
	"twitter_auth_data" : {
		"consumer_key" : "yourconsumerkey",
		"consumer_secret" : "yourconsumersecret",
		"access_token" : "youraccesstoken",
		"access_token_secret" : "youraccesstokensecret"
	},
	"mongo_config" : {
		"host" : "localhost",
		"port" : 27017
	}
}

```