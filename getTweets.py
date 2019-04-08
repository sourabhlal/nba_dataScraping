import ipdb
import json
import tweepy
import time
from twitterAuth import twitter_keys

def initialize_data():
	team_data = {
		'Toronto Raptors': {"handle":'Raptors', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Golden State Warriors': {"handle":'warriors', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Denver Nuggets': {"handle":'nuggets', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'OKC Thunder': {"handle":'okcthunder', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'New Orleans Pelicans': {"handle":'PelicansNBA', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Dallas Mavericks': {"handle":'dallasmavs', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Charlotte Hornets': {"handle":'hornets', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Los Angeles Lakers': {"handle":'Lakers', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'New York Knicks': {"handle":'nyknicks', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Timberwolves': {"handle":'Timberwolves', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'LA Clippers': {"handle":'LAClippers', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Orlando Magic': {"handle":'OrlandoMagic', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Indiana Pacers': {"handle":'Pacers', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Cleveland Cavaliers': {"handle":'cavs', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Houston Rockets': {"handle":'HoustonRockets', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Brooklyn Nets': {"handle":'BrooklynNets', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Phoenix Suns': {"handle":'Suns', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Utah Jazz': {"handle":'utahjazz', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Boston Celtics': {"handle":'celtics', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Atlanta Hawks': {"handle":'ATLHawks', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Detroit Pistons': {"handle":'DetroitPistons', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Chicago Bulls': {"handle":'chicagobulls', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Philadephia 76ers': {"handle":'sixers', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Milwaukee Bucks': {"handle":'Bucks', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Washington Wizands': {"handle":'WashWizards', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Miami HEAT': {"handle":'MiamiHEAT', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Memphis Grizzlies': {"handle":'memgrizz', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Trail Blazers': {"handle":'trailblazers', "tweets":{}, "oldest":{"time":time.time(), "id":0}},
		'Sacramento Kings': {"handle":'SacramentoKings', "tweets":{}, "oldest":{"time":time.time(), "id":0}}
	}

	with open('team_data.json', 'w') as outfile:  
		json.dump(team_data, outfile)

	return team_data


def load_data():
	with open('team_data.json') as json_file:  
		team_data = json.load(json_file)
	return team_data


def tweepy_auth():
	CONSUMER_KEY = twitter_keys['consumer_key']
	CONSUMER_SECRET = twitter_keys['consumer_secret']
	ACCESS_KEY = twitter_keys['access_token']
	ACCESS_SECRET = twitter_keys['access_token_secret']

	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

	api = tweepy.API(auth)

	return api

def get_latest_data(handle):
	tweets = api.user_timeline(handle)
	return tweets

def get_old_Data(team):
	tweets = api.user_timeline(team_data[team]["handle"], max_id=team_data[team]["oldest"]["id"])
	return tweets


INITIALIZATION = False

if INITIALIZATION:
	team_data = initialize_data()
else:
	team_data = load_data()

loopcount = 0
while loopcount < 3:
	loopcount +=1

	api = tweepy_auth()
	for i in team_data.keys():
		handle = team_data[i]["handle"]
		tweets = get_latest_data(handle)
		for t in tweets:
			if t.created_at.timestamp() < team_data[i]["oldest"]["time"]:
				team_data[i]["oldest"]["time"] = t.created_at.timestamp()
				team_data[i]["oldest"]["id"] = t.id
			team_data[i]["tweets"][t.id] = {"time":t.created_at.timestamp(), "RT": t.retweet_count, "fav":t.favorite_count}
		print (i, "complete - loop #", loopcount)

	with open('team_data.json', 'w') as outfile:  
		json.dump(team_data, outfile)
	print ("write complete")
	time.sleep(600)
