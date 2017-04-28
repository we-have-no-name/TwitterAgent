import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import csv, json
from datetime import datetime
import os

class stream_data_storage():
	def __init__(self, file_name, lang='', add_timestamp=True, data_list=None):
		self.lang=lang
		ts=' - ' + datetime.utcnow().strftime('%Y%m%dT%H%M%S') if add_timestamp else ''
		clean_file_name = file_name + ts + '.csv'
		file_name += ts + '.txt'
		if not os.path.exists('Data'): os.makedirs('Data')
		self.stream_data = open('Data/' + file_name, 'w', encoding='utf-8-sig')
		self.stream_data_clean = open('Data/' + clean_file_name, 'w', encoding='utf-8-sig')
		self.sdata_csv_writer = csv.writer(self.stream_data_clean, lineterminator='\n')
		self.data_list=data_list
		
	def write(self, data):
		tweet_json=json.loads(data)
		try:
			if self.lang!='' and tweet_json['lang']!=self.lang: return False
			link='www.twitter.com/' + tweet_json['user']['screen_name'] + '/status/' + str(tweet_json['id'])
			if 'retweeted_status' in tweet_json:
				tweet = "RT @" + tweet_json['retweeted_status']['user']['screen_name'] + ": " + tweet_json['retweeted_status']['text']
			else: tweet = tweet_json['text']
		except KeyError:
			return False
		row=[link, tweet]
		self.sdata_csv_writer.writerow(row)
		self.stream_data.write(data)
		if self.data_list is not None: self.data_list.append(data)
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
		if self.data_handler.write(data): 
			self.count+=1
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
		get_sample_tweets_stream :  get realtime tweets
		get_tweets_stream_with_keywords : get a stream of tweets having the provided keywords (can have emojis)
		search_for_tweets_with_keywords : search for tweets having the specified keyword(s) one keyword at a time (can't have emojis)

'''

class TwitterAgent():
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
		
	
	def make_stream_object(self, file_name, lang='en', add_timestamp=True, max_tweets=20, data_list=None):
		data_handler = stream_data_storage(file_name, lang=lang, add_timestamp=add_timestamp, data_list=data_list)
		self.std_listener = StdOutListener(data_handler, max_tweets=max_tweets)
		stream = Stream(self.auth, self.std_listener)
		return stream
		
	
	def get_sample_tweets_stream(self, file_name='sample_stream_data', lang='en', add_timestamp=True, max_tweets=20, data_list=None):
		"""get a sample from the stream of tweets flowing through Twitter."""
		stream = self.make_stream_object(file_name, lang=lang, add_timestamp=add_timestamp, max_tweets=max_tweets, data_list=data_list)
		stream.sample()
		return data_list
			

	def get_tweets_stream_with_keywords(self, keywords, file_name='stream_data', lang='en', add_timestamp=True, max_tweets=20, data_list=None):
		"""get a stream of tweets having the provided keywords (can have emojis)"""
		stream = self.make_stream_object(file_name, lang=lang, add_timestamp=add_timestamp, max_tweets=max_tweets, data_list=data_list)
		stream.filter(track=keywords)
		return data_list

	def search_for_tweets_with_keywords(self, keywords, lang='en', num_per_keyword=20, result_type='mixed'):
		"""search for tweets having the provided keyword(s) (can't have emojis)"""
		total_keyworded_tweets = []
		for keyword in keywords :
			keyworded_tweets = self.api.search(keyword, count=num_per_keyword, language=[lang], result_type=result_type)
			total_keyworded_tweets.extend(keyworded_tweets)
		return total_keyworded_tweets
		
	def get_tweets_with_ids(self, ids, batch_size=100):
		"""returns full Tweet objects, specified by the ids parameter, max batch_size is 100"""
		tweet_objects = [];
		for i in range(len(ids)//batch_size+bool(len(ids)%batch_size)):
			ids_batch = ids[i*batch_size:min(len(ids), (i+1)*batch_size)]
			tweet_objects += self.api.statuses_lookup(ids_batch)
		return tweet_objects



















