from TwitterAgent import TwitterAgent
import csv, json

def main():
	ta = TwitterAgent()
	#get_sample_stream(ta)
	#search_by_hashtag(ta, ['play'], 100)
	get_stream_tweets_with_keywords(ta, ['\U0001F602'])		#use 16 or 32 bit codes for emoji 
	

def get_sample_stream(ta):
	ta.get_sample_stream_tweets()
	

def get_stream_tweets_with_keywords(ta, keywords):
	ta.get_stream_tweets_with_keywords(keywords)
	

def search_by_hashtag(ta, hashtags, count):
	results=ta.get_hashtag_data(hashtags, num_per_hashtag=count)
	store_search_results(results)
	

def store_search_results(results):
	with open('Data/results.csv', 'w', encoding='utf-8-sig') as csv_file:
		csv_writer = csv.writer(csv_file, lineterminator='\n')
		for t in results:
			link='www.twitter.com/' + t.user.screen_name + '/status/' + str(t.id)
			tweet= t.text
			row=[link, tweet]
			csv_writer.writerow(row)
	with open('Data/results_full.json', 'w', encoding='utf-8-sig') as json_full_file:
		json_full_file.write(json.dumps(str(results), ensure_ascii=False))	
	with open('Data/results.json', 'w', encoding='utf-8-sig') as json_file:
		for i in range(len(results)):
			results[i]=results[i]._json
		json_file.write(json.dumps(results, ensure_ascii=False))		
		

if __name__ == "__main__": main()
