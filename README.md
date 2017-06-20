# TwitterAgent
---
simple twitter agent to help collect tweets for our Data set

### Requirements
you need to make a simple config.json file with this structure  
those credentials can be optained after creating an app in https://apps.twitter.com
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
---
### Example usage
```python
import TwitterAgent
agent = TwitterAgent.TwitterAgent()
# get sample data
agent.get_sample_tweets_stream()
# get data with specific keywords
agent.get_with_keywords(['play'], 100)
# get stream data with specific keywords
agent.get_tweets_stream_with_keywords(['\U0001F602'])
# get stream data with specific keywords (phrases)
agent.get_tweets_stream_with_keywords(['the are'])
```