import csv, json


def main():
	data = parse_data('Data/results.json')
	
	test_file = open('Data/test.csv', 'w', encoding='utf-8-sig')
	csv_writer=csv.writer(test_file, lineterminator='\n')
	for tweet in data:
		link = 'www.twitter.com/' + tweet['user']['screen_name'] + '/status/' + str(tweet['id'])
		tweet = tweet['text']
		print(link)
		csv_writer.writerow([link, tweet])
	test_file.close()
	     
def parse_data(file_name):
	with open(file_name, 'r', encoding='utf-8-sig') as json_file:
		data = json.load(json_file)
		return data


if __name__ == "__main__": main()
 
