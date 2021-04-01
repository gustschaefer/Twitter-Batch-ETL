import tweepy
import json
from datetime import date, datetime
import time

CONSUMER_KEY = "bj1HxgkRGzDZTqKZbd5bZxsCT"
CONSUMER_SECRET = "rgouf15ueg5Q6Jc0Z1JpUpoYYghs8GZITVs7pZmSw9Dvcto60B"
ACCESS_TOKEN = "1376541401396224000-W9K7oeHJ4QWZPilBYKkK7ued1QlJbe"
ACCESS_TOKEN_SECRET = "TyiBFblzpsNsV0r3FL14OHRYbq7XIdatrzQyPBuWsh3jd"

# BEARER_TOKEN = AAAAAAAAAAAAAAAAAAAAAGFvOAEAAAAAvFpjI7ifq6e6kTlkaSDagc7H%2B0c%3DBRsDSD3ntbQLniTccFCoMEFYHGUlEKa4L6Myo50pHQOwDHdxzd


def initialize_tweepy(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth, wait_on_rate_limit=True, 
						   wait_on_rate_limit_notify=True, retry_count=5, retry_delay=10)
	return api

def get_trending_topics(local_id, num_trends=-1, min_volume=1000):
	# By using num_trends = -1 we can get every available trend

	# Get available trends in Brazil
	local_trends = api.trends_place(id=local_id)
	# Get treinds 
	local_trends = local_trends[0]['trends']
	# List will store the trend name and volume
	trends_infos = []

	# Get trend names and volume
	for trend in local_trends: 
	    if trend['tweet_volume'] is not None and trend['tweet_volume'] > min_volume: 
	        trends_infos.append((trend['name'], trend['tweet_volume']))

	# Sort trends
	trends_infos.sort(key=lambda x:-x[1])
	# Get Top {num_trends} trends
	trending_topics = trends_infos[:num_trends]
	return trending_topics

def search_trend(topic, api, lang, num_tweets, result_type):

	top_tweets = tweepy.Cursor(api.search, q=topic, 
							   tweet_mode="extended", 
							   rpp=num_tweets,
	                           result_type=result_type,
	                           since=date.today(),
	                           include_entities=True, 
	                           lang=lang).items(num_tweets)
	return top_tweets

def parse_tweet_data(tweet_text):
	tweets_list = []
	for tweet in tweet_text:
		tweets_data = {
			"ID" : tweet.id,
			"User" : tweet.user.screen_name,
			"UserName" : tweet.user.name,
			"UserLocation" : tweet.user.location,
			"TweetText" : tweet.full_text.replace("\n", " ").replace("\"", " "),
			"Language" : tweet.user.lang,
			"Date" : tweet.created_at,
			"Source": tweet.source,
			"Likes" : tweet.favorite_count,
			"Retweets" : tweet.retweet_count,
			"Coordinates" : tweet.coordinates,
			"Place" : tweet.place
		}
		tweets_list.append(tweets_data)
	return tweets_list

def create_final_data(api, trending_topics, lang="en", num_tweets=5, result_type="mixed"):
	# Return tweets about a topic

	final = []
	for topic in trending_topics:
		trend_name = topic[0]
		trend_volume = topic[1]
		# Get top 3 tweets about this topic
		top_tweets = search_trend(trend_name, api, lang, num_tweets=num_tweets, result_type=result_type)
		# Extract most important infos about the tweets 
		top_tweets_infos = parse_tweet_data(top_tweets)
		final_info = {
			"Trending name": trend_name,
			"Volume": trend_volume,
			"Trending Date": date.today(),
			"Top Tweets": top_tweets_infos
		}
		final.append(final_info)

	return final

def get_country_id(api, country_name):
	
	woeid = {
			"UK": {"id": 23424975, "lang": "en"},
			"Brazil": {"id": 23424768, "lang": "pt"},
			"Germany": {"id": 23424829, "lang": "en"}, 
			"Canada": {"id": 23424775, "lang": "en"},
			"USA": {"id": 23424977, "lang": "en"},
			"Sweden": {"id": 23424954, "lang": "en"},
			}

	return woeid[country_name]

def save_json_file(json_data, file_name=f'TweetsData-{date.today()}.json'):
	with open("./tweets-data/json/"+file_name, 'w', encoding='utf-8') as f:
		json.dump(json_data, f, indent=4, default=str, ensure_ascii=False)

# Initialize TweePy API
api = initialize_tweepy(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# We will use these countries, but you can add more
countries = ["UK", "Brazil", "Germany", "Canada", "USA", "Sweden"]

for country in countries:
	# Get country id and lang
	c_id = get_country_id(api, country)
	# Return trending topics of the country
	trending_topics = get_trending_topics(c_id["id"])
	# Get five tweets about each trending topic of the country
	json_tweets = create_final_data(api, trending_topics, lang=c_id["lang"])
	# Create a json file for the country, ex.: TweetDataBrasil-2021-03-30.json
	file_name = f'TweetsData-{country}-{date.today()}.json'
	# Save json file in disk
	save_json_file(json_tweets, file_name=file_name)

	print(f"{country} file created!")

# Extraction workflow
# initialize_tweepy() >> get_trending_topics() >> create_final_data() >> save_json_file
