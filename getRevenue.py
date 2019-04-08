from webbot import Browser
from bs4 import BeautifulSoup
import requests
import time
import csv
import ipdb
import pandas as pd
import itertools


def clean_numbers(number):
	number = number.replace('$', '')
	number = number.replace(' ', '')

	if number[-1] == 'K':
		number = float(number[:-1])*1000
	elif number[-1] == 'M':
		number = float(number[:-1])*1000000
	elif number[-1] == 'B':
		number = float(number[:-1])*1000000000
	
	return number

def clean_percentage(x):
    return float(x.strip('%'))/100

def extractData(url):
	print ("TIMESTAMP", url[28:-43])

	web = Browser()
	web.go_to(url)
	time.sleep(10)

	data = web.get_page_source()
	soup = BeautifulSoup(data, features="lxml")

	year = soup.find("li", class_="ranking").a.contents
	print ("YEAR", year[0][:4])

	table = soup.select("#list-table-body")


	scroll_counter = 8

	while len(table[0].findAll('tr')) < 30:
		web.scrolly(1000)
		time.sleep(2)
		data = web.get_page_source()
		soup = BeautifulSoup(data, features="lxml")
		table = soup.select("#list-table-body")
		
		scroll_counter-= 1

		if scroll_counter == 0:
			web.quit()
			return []

	web.quit()

	rows = table[0].findAll('tr')

	ret_list = []

	for r in rows:

		cols = r.findAll('td')
		if 'ad' in cols[0].get("class"):
			continue
		else:
			row_data = {}
			row_data['year'] = year[0][:4]
			row_data['timestamp'] = url[28:-43]
			#current rank
			row_data['rank'] = cols[1].contents[0][1:]

			#teamname
			row_data['name'] = cols[2].a.contents[0]

			#current value
			row_data['val'] = clean_numbers(cols[3].contents[0])

			#one year value change percentage
			row_data['oneyear'] = clean_percentage(cols[4].contents[0])

			#debt value
			row_data['debt'] = clean_percentage(cols[5].contents[0])

			#revenue
			row_data['revenue'] = clean_numbers(cols[6].contents[0])

			#income
			row_data['income'] = clean_numbers(cols[7].contents[0])

			ret_list.append(row_data)

	return ret_list



#load urls
with open('wbmachine.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	next(reader)
	data = [r[0] for r in reader]
csvFile.close()

final_data_list = []

while len(data) > 0:
	url = data.pop(0)
	ret = extractData(url)
	if len(ret)==0:
		data.append(url)
	else:
		final_data_list.extend(ret)

dataframe = pd.DataFrame.from_records(final_data_list)

dataframe.to_csv ('incomedata.csv', index = None, header=True)
dataframe.to_hdf('incomedata.h5', key='dataframe', mode='w')


