from TwitterAgent import TwitterAgent
import csv, json

def main():
	ta = TwitterAgent()
	#get_sample_stream(ta)
	search_by_hashtag(ta, ['play'], 100)



def get_sample_stream(ta):
	try:
		ta.get_sample_stream_tweets()
	except:
		pass

def search_by_hashtag(ta, hashtags, count):
	tweets=ta.get_hashtag_data(['play'], num_per_hashtag=count)
	with open('Data/results.csv', 'w', encoding='utf-8-sig') as csv_file:
		csv_writer = csv.writer(csv_file, lineterminator='\n')
		for t in tweets:
			link='twitter.com/' + str(t.user.id) + '/status/' + str(t.id)
			tweet= t.text
			row=[link, tweet]
			csv_writer.writerow(row)
	with open('Data/results.json', 'w', encoding='utf-8-sig') as json_file:
		for i in range(len(tweets)):
			tweets[i]=tweets[i]._json
		json_file.write(json.dumps(tweets, ensure_ascii=False))

			

if __name__ == "__main__": main()
