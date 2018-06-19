import re, sys, threading
from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup

'''Constant url'''
url = 'https://www.youtube.com/results?search_query='

def crawler(inputs):
	'''Driver'''
	driver = webdriver.Chrome('./chromedriver')
	driver.get(inputs)

	'''Analyze page source'''
	source = driver.page_source
	data = source.split('<script>')

	for i in range(len(data)):
		if data[i].find('twoColumnSearch') != -1:
				data = data[i]
				break

	'''Filting data'''
	data = data[data.find('itemSectionRenderer'):data.find('continuation') - 2]

	urldata = []
	rowdata = []
	urldata = re.findall('/watch.+?"', data)
	for i in range(len(urldata)):
		if urldata[i].find(' ') != -1:
			urldata[i] = urldata[i][:urldata[i].find(' ')]

	rowdata = re.findall('"title":{"accessibility".+?}}', data)
	rowdata = [re.sub('"title".+?"label":', '', x) for x in rowdata]
	rowdata = [re.sub('}}', '', x) for x in rowdata]
	rowdata = [re.sub(r'\\u0026', '', x) for x in rowdata]

f = open('LSA.txt', 'r')
req = [threading.Thread(target = crawler, args = (text)) for text in f.realines()]

for i in range(len(req)):
	req[i].start()
