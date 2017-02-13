import tweepy, csv 
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json


class StdOutListener(StreamListener):

	def __init__(self, file_name, clean_file_name, max_tweets=-1):
		self.count=0
		self.max_tweets=max_tweets
		self.stream_data = open('Data/' + file_name, 'w', encoding='utf-8-sig')
		self.stream_data_clean = open('Data/' + clean_file_name, 'w', encoding='utf-8-sig')
		self.sdata_csv_writer = csv.writer(self.stream_data_clean, lineterminator='\n')

	def on_data(self, data):
		self.stream_data.write(data)
		tweet_json=json.loads(data)
		try:
			link='www.twitter.com/' + tweet_json['user']['screen_name'] + '/status/' + str(tweet_json['id'])
			tweet= tweet_json['text']
			row=[link, tweet]
			self.sdata_csv_writer.writerow(row)
		except KeyError:
			pass
		self.count+=1
		if self.max_tweets!=-1 and self.count>=self.max_tweets: return False
		return True

	def on_error(self, status):
		print(status)

	def __exit__(self, exc_type, exc_value, traceback):
		self.stream_data.close()


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
	def __init__(self, config_file='config.json'):
		try:
			with open(config_file) as json_config_file:
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
		
	
	def make_stream_object(self, file_name, clean_file_name):
		self.std_listener = StdOutListener(file_name, clean_file_name, max_tweets=20)
		stream = Stream(self.auth, self.std_listener)
		return stream
		
	
	def get_sample_stream_tweets(self):
		stream = self.make_stream_object('sample_stream_data.txt', clean_file_name='sample_stream_data_clean.csv')
		return stream.sample()
			
	
	#supports emoji	
	def get_stream_tweets_with_keywords(self, keywords):
		stream = self.make_stream_object('stream_data.txt', clean_file_name='stream_data_clean.csv')
		return stream.filter(track=keywords)

	#doesn't support emoji
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

	




















