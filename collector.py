from TwitterAgent import TwitterAgent
import csv, json
from datetime import datetime

def main():
	ta = TwitterAgent()
	#get_sample_tweets_stream(ta)
	#get_tweets_list_with_hashtags(ta, ['play'], 100)
	#get_tweets_stream_with_keywords(ta, ['\U0001F602'])		#use 16 or 32 bit codes for unicode (e.g. emoji) 
	#get_tweets_stream_with_keywords(ta, ['the are'])			#Spaces are ANDs, commas are ORs
	

def get_sample_tweets_stream(ta):
	ta.get_sample_tweets_stream()
	

def get_tweets_stream_with_keywords(ta, keywords):
	ta.get_tweets_stream_with_keywords(keywords)
	

def get_tweets_list_with_hashtags(ta, hashtags, count):
	results=ta.get_tweets_list_with_hashtags(hashtags, num_per_hashtag=count)
	store_hashtag_data(results)
	

def store_hashtag_data(results):
	ts=' - ' + datetime.utcnow().strftime('%Y%m%dT%H%M%S')
	with open('Data/results' + ts + '.csv', 'w', encoding='utf-8-sig') as csv_file:
		csv_writer = csv.writer(csv_file, lineterminator='\n')
		for t in results:
			link='www.twitter.com/' + t.user.screen_name + '/status/' + str(t.id)
			tweet= t.text
			row=[link, tweet]
			csv_writer.writerow(row)
	with open('Data/results_full' + ts + '.json', 'w', encoding='utf-8-sig') as json_full_file:
		json_full_file.write(json.dumps(str(results), ensure_ascii=False))	
	with open('Data/results' + ts + '.json', 'w', encoding='utf-8-sig') as json_file:
		for i in range(len(results)):
			results[i]=results[i]._json
		json_file.write(json.dumps(results, ensure_ascii=False))		
		

if __name__ == "__main__": main()
