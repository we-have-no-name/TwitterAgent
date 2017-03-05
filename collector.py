from TwitterAgent import TwitterAgent
import csv, json, pickle
import os
from datetime import datetime

def main():
	ta = TwitterAgent()
	#get_sample_tweets_stream(ta)
	#search_for_tweets_with_keywords(ta, ['play'], 100)
	#get_tweets_stream_with_keywords(ta, ['\U0001F602'])
	#get_tweets_stream_with_keywords(ta, ['the are'])
	

def get_sample_tweets_stream(ta, file_name='sample_stream_data', lang='en', add_timestamp=True, max_tweets=20, data_list=None):
	ta.get_sample_tweets_stream(file_name=file_name, lang=lang, add_timestamp=add_timestamp, max_tweets=max_tweets, data_list=data_list)
	

def get_tweets_stream_with_keywords(ta, keywords, file_name='stream_data', lang='en', add_timestamp=True, max_tweets=20, data_list=None):
	"""
	use 16 or 32 bit codes for unicode (e.g. emoji='\U0001F602')
	Spaces are ANDs, commas are ORs
	pass a data list to append stream data to
	"""
	ta.get_tweets_stream_with_keywords(keywords, file_name=file_name, lang=lang, add_timestamp=add_timestamp, max_tweets=max_tweets, data_list=data_list)
	

def search_for_tweets_with_keywords(ta, keywords, lang='en', num_per_keyword=20, result_type='mixed'):
	results=ta.search_for_tweets_with_keywords(keywords, lang=lang, num_per_keyword=num_per_keyword, result_type=result_type)
	#result_type: mixed, recent or popular
	store_list_of_objects(results)
	

def store_list_of_objects(results):
	ts=' - ' + datetime.utcnow().strftime('%Y%m%dT%H%M%S')
	if not os.path.exists("Data"): os.makedirs("Data") 
	with open('Data/results' + ts + '.csv', 'w', encoding='utf-8-sig') as csv_file:
		csv_writer = csv.writer(csv_file, lineterminator='\n')
		for t in results:
			link='www.twitter.com/' + t.user.screen_name + '/status/' + str(t.id)
			tweet= t.text
			row=[link, tweet]
			csv_writer.writerow(row)
	with open('Data/results_full' + ts + '.pickle', 'wb') as pickle_full_file:
		pickle.dump(results, pickle_full_file)
	with open('Data/results' + ts + '.json', 'w', encoding='utf-8-sig') as json_file:
		for i in range(len(results)):
			results[i]=results[i]._json
		json.dump(results, json_file, ensure_ascii=False)
		

if __name__ == "__main__": main()
