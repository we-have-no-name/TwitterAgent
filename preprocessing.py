import json
import csv
import re
def main():
    tweets_file = open('dataset3.txt', "r")
    csv_file= open( "data3.csv", "w" ,encoding='utf-8-sig')
    wtr= csv.writer( csv_file,delimiter='\t' ,lineterminator='\n' )
    for line in tweets_file:
        try:
            tweet = json.loads(line.strip())
            if 'text' in tweet:
                link = 'www.twitter.com/' + tweet['user']['screen_name'] + '/status/' + str(tweet['id'])
                tweet1 = tweet['text']
                tweet1 = remove_rt(tweet1)
                tweet1 = remove_link(tweet1)
                tweet1 = remove_mentions(tweet1)
                tweet1 = remove_repeated_chars(tweet1)
                tweet1 = modify_lowercase_uppercase(tweet1) 
                wtr.writerow([link, tweet1])
        except:
            continue
            
def remove_rt(txt):
    txt = txt.replace('RT','')
    return txt
    
def remove_link(txt):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', txt)
    for i in range(len(urls)):
        txt=txt.replace(urls[i],'')
    return txt
    
def remove_mentions(txt):
    mentions = re.findall(r'(?<=\W)[@]\S*', txt)
    for i in range(len(mentions)):
        txt=txt.replace(mentions[i],'')
    return txt
    
def remove_repeated_chars(txt):
    repeated_char= re.findall(r'((\w)\2{2,})',txt)
    for i  in range(len(repeated_char)):
        txt = txt.replace(repeated_char[i][0],repeated_char[i][1])
    return txt
    
def modify_lowercase_uppercase(txt):
    text = txt.split(' ')
    for j in range(len(text)):
        if not(text[j].isupper()) and not(text[j].islower()):
            text[j] = text[j].lower()
    tweet = ' '.join(text )
    return tweet

if __name__ == "__main__": main()