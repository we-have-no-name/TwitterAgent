# TwitterAgent
simple twitter agent to help us in making the Data set 

you nead to make a simple config.json file with this structure
```json

{

	"consumer_key": "",
	"consumer_secret": "",

	"access_token":"",
	"access_token_secret":""
}


```


and pass it to the TwitterAgent object 



```python

agent = TwitterAgent("config.json")

```

to collect data you will need to use the Collector class 

```python

c = Collector()
# get sample data
c.get_sample_tweets_stream()
# get data with specific keywords
c.get_with_keywords(['play'], 100)
# get stream data with specific keywords
c.get_tweets_stream_with_keywords(['\U0001F602'])
# get stream data with specific keywords (phrases)
c.get_tweets_stream_with_keywords(['the are'])

```