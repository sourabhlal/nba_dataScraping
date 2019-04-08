## Popularity of NBA teams

We are interested in the following question: does the popularity of a NBA team correlate with its profitability?

### Aim

Acquire data from various sources, structure and consolidate them to build indicators for the popularity and profitability of a NBA team.

### Method

* In order to access data on profitability, we got the data for all NBA teams from [Forbes](https://www.forbes.com/nba-valuations/list/). This site has been updated with the latest data over the past several years. Therefore to access older versions of this page, we scrape the [Internet Archive (wayback machine)](https://archive.org/web/).
* In order to access data on popularity, we look at the tweet engagements for the various NBA teams. (In particular number of 'favorites' and number of 'retweets')

### Code

* `getTweets.py` - this script collects tweets - it uses Twitter APIs to get recent tweets by each team and saves to json
* `waybackMachineScript.py` - this script scrapes wayback machine for all snapshots of the Forbes data
* `getRevenue.py` - this uses the urls aquired from wayback machine and collects data about income and revenue from each snapshot and saves to pandas dataframe

### Data

* `team_data.json` - tweet data collected
* `wbmachine.csv` - urls collected from waybackmachine
* `incomedata.h5` - income and revenue data
* `incomedata.csv` - duplicate of *incomedata.h5*, included for readibility 


### Instructions to run scripts
* `getTweets.py`
	* First time set `INITIALIZATION` variable to True, if starting from scratch. If adding more data, set to False.
	* Create a new file in same directior called `twitterAuth.py`. Within this file add a dict called `twitter_keys`. In this dict store the API keys (`consumer_key`, `consumer_secret`, `access_token`, `access_token_secret`)from your Twitter Dev Account.
* The other scripts are ready to run. Just make sure to install all dependancies.