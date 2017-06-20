from TwitterAgent import TwitterAgent

def main():
	ta = TwitterAgent()
##	ta.get_sample_tweets_stream()
##	ta.search_for_tweets_with_keywords(['play'], 100)
##	ta.get_tweets_stream_with_keywords(['\U0001F602'])
##	ta.get_tweets_stream_with_keywords(['the are'])
	ta.get_tweets_with_ids([432656548536401920])


if __name__ == "__main__": main()
