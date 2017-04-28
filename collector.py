from TwitterAgent import TwitterAgent
import csv, json, pickle
import os
from datetime import datetime

def main():
	c = collector()
##	c.get_sample_tweets_stream()
##	c.search_for_tweets_with_keywords(['play'], 100)
##	c.get_tweets_stream_with_keywords(['\U0001F602'])
##	c.get_tweets_stream_with_keywords(['the are'])
##	c.get_tweets_with_ids([432656548536401920])
	
class collector():
	def __init__(self):
		self.ta=TwitterAgent()
		
	def get_sample_tweets_stream(self, file_name='sample_stream_data', lang='en', add_timestamp=True, max_tweets=20, data_list=None):
		self.ta.get_sample_tweets_stream(file_name=file_name, lang=lang, add_timestamp=add_timestamp, max_tweets=max_tweets, data_list=data_list)
		

	def get_tweets_stream_with_keywords(self, keywords, file_name='stream_data', lang='en', add_timestamp=True, max_tweets=20, data_list=None):
		"""
		use 16 or 32 bit codes for unicode (e.g. emoji='\U0001F602')
		Spaces are ANDs, commas are ORs
		pass a data list to append stream data to
		"""
		self.ta.get_tweets_stream_with_keywords(keywords, file_name=file_name, lang=lang, add_timestamp=add_timestamp, max_tweets=max_tweets, data_list=data_list)
		

	def search_for_tweets_with_keywords(self, keywords, lang='en', num_per_keyword=20, result_type='mixed'):
		results=self.ta.search_for_tweets_with_keywords(keywords, lang=lang, num_per_keyword=num_per_keyword, result_type=result_type)
		#result_type: mixed, recent or popular
		self.store_list_of_objects(results)
		return results
		
	def get_tweets_with_ids(self, ids,  batch_size=100):
		"""returns full Tweet objects, specified by the ids parameter, max batch_size is 100"""
		results=self.ta.get_tweets_with_ids(ids, batch_size=batch_size)
		self.store_list_of_objects(results)
		return results

	def store_list_of_objects(self, results):
		ts=' - ' + datetime.utcnow().strftime('%Y%m%dT%H%M%S')
		if not os.path.exists("Data"): os.makedirs("Data") 
		with open('Data/results' + ts + '.csv', 'w', encoding='utf-8-sig') as csv_file:
			csv_writer = csv.writer(csv_file, lineterminator='\n')
			for t in results:
				link='www.twitter.com/' + t.user.screen_name + '/status/' + str(t.id)
				if hasattr(t, 'retweeted_status'):
					tweet = "RT @" + t.retweeted_status.user.screen_name + ": " + t.retweeted_status.text
				else: tweet = t.text
				row=[link, tweet]
				csv_writer.writerow(row)
		with open('Data/results_full' + ts + '.pickle', 'wb') as pickle_full_file:
			pickle.dump(results, pickle_full_file)
		with open('Data/results' + ts + '.json', 'w', encoding='utf-8-sig') as json_file:
			results_json=[]
			for i in range(len(results)):
				results_json.append(results[i]._json)
			json.dump(results_json, json_file, ensure_ascii=False)
		

if __name__ == "__main__": main()
