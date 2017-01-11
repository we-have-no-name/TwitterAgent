import tweepy, csv 
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json


class StdOutListener(StreamListener):

	def on_data(self, data):
		print(data)
		return True

	def on_error(self, status):
		print(status)


'''
	TwitterAgent is a simple class that works as a wrapper 
	for dealing with tweets and data from twitter and make your
	own dataset
	functions:
		make_stream_object : make a tweepy streemobject
		get_sample_stream_tweats :  gets realtime tweets
		get_hashtag_data : gets hashtaged tweets

'''

class TwitterAgent(object):
	def __init__(self, config_file):
		try:
			with open('config.json') as json_config_file:
				data = json.load(json_config_file)
				self.consumer_key = data['consumer_key']
				self.consumer_secret = data['consumer_secret']
				self.access_token = data['access_token']
				self.access_token_secret = data['access_token_secret']

			self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
			self.auth.set_access_token(self.access_token, self.access_token_secret)
			self.api = tweepy.API(self.auth)
		except :
			print("invaild data for auth")


	def make_stream_object(self):
		self.std_listener = StdOutListener()
		stream = Stream(self.auth, self.std_listener)
		return stream


	def get_sample_stream_tweets(self):
		stream = self.make_stream_object()
		return stream.sample()


	def get_hashtag_data(self, hashtags, num_per_hashtag=20):
		total_hashtaged_tweets = []
		for hashtag in hashtags :
			hashtag_tweets = self.api.search(hashtag, count=num_per_hashtag, language=["en"])
			total_hashtaged_tweets.extend(hashtag_tweets)
		return total_hashtaged_tweets


	def get_emoticon_data(self, emoticons):
		raise NotImplemented

	def export_to_csv(self):
		raise NotImplemented

	



















