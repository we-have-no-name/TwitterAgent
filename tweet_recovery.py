import csv, pickle, json
from collector import collector
import os, sys

def main():
	csv_o = tweet_recovery()
	csv_o.csv_tweet_recover(r"tweets.csv", fetch_online=True)
	
class tweet_recovery():
	def __init__(self):
		self.c = collector()

	def csv_tweet_recover(self, csv_file_name='tweets.csv', pickle_file_name='tweets.pickle', json_txt_file_name = 'tweets.txt',csv_src_file_name = 'tweets_src.csv', fetch_online=False):
		rows = self.csv_to_list(csv_file_name)
		if os.path.isfile(pickle_file_name):
			id_tweet_map = self.id_tweet_map_from_pickle(pickle_file_name)
		elif os.path.isfile(json_txt_file_name):
			id_tweet_map = self.id_tweet_map_from_json_txt(json_txt_file_name)
		elif os.path.isfile(csv_src_file_name):
			id_tweet_map = self.id_tweet_map_from_csv(csv_src_file_name)
		elif fetch_online:
			id_tweet_map = self.id_tweet_map_from_tweet_objects(self.csv_to_full_objects(csv_file_name, 100))
		else:
			print("add a reset source file or set fetch_online=True \nexiting.")
			sys.exit(0)
		for row in rows:
			if row[1]=="": continue
			tweet_id, = self.links_to_tweet_ids([row[0]])
			row[1] = id_tweet_map.get(tweet_id, row[1])
		out_csv_file_name = os.path.splitext(csv_file_name)[0] + "_out.csv"
		self.list_to_csv(rows, out_csv_file_name)
		return True
                        
	def csv_to_full_objects(self, csv_file_name='tweets.csv', batch_size = 100):
		"""returns full Tweet objects, specified by the ids parameter, max batch_size is 100"""
		rows = self.csv_to_list(csv_file_name)
		tweet_ids = self.links_to_tweet_ids([row[0] for row in rows if row[1]!=""])
		return self.c.get_tweets_with_ids(tweet_ids, batch_size = batch_size)

	def id_tweet_map_from_pickle(self, pickle_file_name='tweets.pickle'):
		pickle_file = open(pickle_file_name, 'rb')
		pickle_object = pickle.load(pickle_file)
		pickle_file.close()
		return self.id_tweet_map_from_tweet_objects(pickle_object)

	def id_tweet_map_from_tweet_objects(self, pickle_object):
		id_tweet_map = dict()
		for status in pickle_object:
			status_id  = status.id
			if hasattr(status, 'retweeted_status'):
				tweet = "RT @" + status.retweeted_status.user.screen_name + ": " + status.retweeted_status.text
			else: tweet = status.text
			id_tweet_map[status_id] = tweet
		return id_tweet_map

	def id_tweet_map_from_csv(self, csv_file_name='tweets_src.csv'):
		csv_file = open(csv_file_name, encoding='utf-8-sig')
		csv_reader = csv.reader(csv_file)
		id_tweet_map = dict()
		for row in csv_reader:
			if row[1]=="": continue
			tweet_id, = self.links_to_tweet_ids([row[0]])
			id_tweet_map[tweet_id] = row[1]
		csv_file.close()
		return id_tweet_map

	def id_tweet_map_from_json_txt(self, json_txt_file_name='tweets.json'):
		"""assumes the file is composed of json strings, each tweet json in one line"""
		json_txt_file = open(json_txt_file_name, encoding='utf-8-sig')
		id_tweet_map = dict()
		for line in json_txt_file:
			if len(line)==1: continue
			status = json.loads(line)
			status_id  = status['id']
			if 'retweeted_status' in status:
				tweet = "RT @" + status['retweeted_status']['user']['screen_name'] + ": " + status['retweeted_status']['text']
			else: tweet = status['text']
			id_tweet_map[status_id] = tweet
		json_txt_file.close()
		return id_tweet_map
			

	def links_to_tweet_ids(self, links):
		tweet_ids=[]
		for link in links:
			try:
				tweet_id = int(link.split(r'/')[3])
			except IndexError as e:
				print("csv format error \ncheck for unquoted multi line rows using carriage return as line terminator \n" + link + "\nexiting")
				sys.exit(0)
			tweet_ids.append(tweet_id)
		return tweet_ids

	def csv_to_list(self, csv_file_name='tweets.csv'):
		csv_file = open(csv_file_name, encoding='utf-8-sig')
		csv_reader = csv.reader(csv_file)
		rows=[]
		for row in csv_reader:
			if len(row)==0: continue
			rows.append(row)
		csv_file.close()
		return rows

	def list_to_csv(self, rows, csv_file_name='tweets.csv'):
		csv_file = open(csv_file_name, 'w', encoding='utf-8-sig')
		csv_writer = csv.writer(csv_file)
		csv_writer.writerows(rows)
		csv_file.close()
		return True


if __name__ == "__main__": main()
