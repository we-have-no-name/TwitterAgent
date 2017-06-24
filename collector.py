from TwitterAgent import TwitterAgent
from queue import Queue
import threading, time

def main():
	ta = TwitterAgent()
##	ta.get_sample_tweets_stream()
##	ta.search_for_tweets_with_keywords(['play'], num_per_keyword=100)
##	ta.get_tweets_stream_with_keywords(['\U0001F602'])
##	ta.get_tweets_stream_with_keywords(['the are'])
##	ta.get_tweets_with_ids([432656548536401920])
##	background_service_example(ta)

def background_service_example(ta):	
	q = Queue()
	max_tweets=[-1]
	def task(q):
		ta.get_tweets_stream_with_keywords(['\U0001F602'], max_tweets=max_tweets, data_handler=q, save_to_files=False)
		
	t = threading.Thread(target=task, args = (q,))
	t.start()
	while(t.is_alive()):
		print('Queue Length={}'.format(len(q.queue)))
		time.sleep(1)
		# stopping the stream from any thread
		if(len(q.queue)>30):
			max_tweets[0]=0

if __name__ == "__main__": main()
