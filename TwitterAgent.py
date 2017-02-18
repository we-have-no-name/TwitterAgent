import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv, json
from datetime import datetime

class stream_data_storage():
	def __init__(self, file_name, lang='', add_ts=True, data_list=[]):
		self.lang=lang
		ts=' - ' + datetime.utcnow().strftime('%Y%m%dT%H%M%S') if add_ts else ''
		clean_file_name = file_name + ts + '.csv'
		file_name += ts + '.txt'
		self.stream_data = open('Data/' + file_name, 'w', encoding='utf-8-sig')
		self.stream_data_clean = open('Data/' + clean_file_name, 'w', encoding='utf-8-sig')
		self.sdata_csv_writer = csv.writer(self.stream_data_clean, lineterminator='\n')
		self.data_list=data_list
		
	def write(self, data):
		tweet_json=json.loads(data)
		try:
			if self.lang!='' and tweet_json['lang']!=self.lang: return False
			link='www.twitter.com/' + tweet_json['user']['screen_name'] + '/status/' + str(tweet_json['id'])
			tweet= tweet_json['text']
		except KeyError:
			return False
		row=[link, tweet]
		self.sdata_csv_writer.writerow(row)
		self.stream_data.write(data)
		return True
		
	def store_to_list(self, data):
		self.data_list.append(data)
		return True
		
	def __exit__(self, exc_type, exc_value, traceback):
		self.stream_data.close()
		self.stream_data_clean.close()



class StdOutListener(StreamListener):
	
	def __init__(self, data_handler, max_tweets=-1):
		self.count=0
		self.max_tweets=max_tweets
		self.data_handler=data_handler

	def on_data(self, data):
		if self.data_handler.write(data): self.count+=1
		if self.max_tweets!=-1 and self.count>=self.max_tweets: return False
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
		
	
	def make_stream_object(self, file_name):
		data_handler = stream_data_storage(file_name, lang='en', add_ts=True)
		self.std_listener = StdOutListener(data_handler, max_tweets=20)
		stream = Stream(self.auth, self.std_listener)
		return stream
		
	
	def get_sample_stream_tweets(self):
		stream = self.make_stream_object('sample_stream_data')
		return stream.sample()
			
	
	#supports emoji	
	def get_stream_tweets_with_keywords(self, keywords):
		stream = self.make_stream_object('stream_data')
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

	




















