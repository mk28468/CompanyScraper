import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as BS4
import time

USERNAME = 
PASSWORD = 

class Scrapper(object):
	def __init__(self):
		self.driver = webdriver.Chrome(executable_path="./chromedriver")
		self.wait = WebDriverWait(self.driver, 10)
		self.page_source = ''
		self.login()

	def login(self):
		try:
			self.driver.get("http://www.glassdoor.com/profile/login_input.htm")
			user_login = self.wait.until(EC.presence_of_element_located( (By.NAME, "username")))
			pw_login = self.driver.find_element_by_class_name("signin-password")
			login_button = self.driver.find_element_by_id("signInBtn")
			user_login.send_keys(USERNAME)
			user_login.send_keys(Keys.TAB)
			time.sleep(0.5)
			pw_login.send_keys(PASSWORD)
			time.sleep(0.5)
			login_button.click()

		except TimeoutException:
			print("TimeoutException! Username/password field or login button not found on glassdoor.com")
			exit()

	def fetch_overview_page(self, url):
		try:
			#time.sleep(2)
			self.driver.get(url)
			#time.sleep(2)
			self.page_source = self.driver.page_source
			return self.driver.page_source
		except TimeoutException:
			print('An error occured, Please check if url is correct.')
			exit()


	def parse_overview_data(self):
		data = []
		soup = BS4(self.page_source, "html.parser")
		if(soup.find('h1', {'class': ' strong tightAll'})):
			name = soup.find('h1', {'class': ' strong tightAll'}).text.strip()

		overview = soup.find('div', {'class': 'info flexbox row col-hh'})

		infos = overview.find_all('div', {'class': 'infoEntity'})
		website = ''
		hq = ''
		size = ''
		founded = ''
		industry = ''
		revenue = ''

		for info in infos:
			if 'Website' in info.text:
				website = info.find('a', {'class': 'link'}).text.strip()
			elif 'Headquarters' in info.text:
				hq = info.find('span', {'class': 'value'}).text.strip()
			elif 'Size' in info.text:
				size = info.find('span', {'class': 'value'}).text.strip()
			elif 'Founded' in info.text:
				founded = info.find('span', {'class': 'value'}).text.strip()
			elif 'Type' in info.text:
				type = info.find('span', {'class': 'value'}).text.strip()
			elif 'Industry' in info.text:
				industry = info.find('span', {'class': 'value'}).text.strip()
			elif 'Revenue' in info.text:
				revenue = info.find('span', {'class': 'value'}).text.strip()

			#print"***print info over"
		review = {
			'Name':name,
			'Website': website,
			'Headquarters': hq,
			'Size': size,
			'Founded': founded,
			'Type': type,
			'Industry': industry,
			'Revenue': revenue
			}

		data.append(review)

		return data

	def fetch_review_page(self):
		time.sleep(4)
		soup = BS4(self.page_source, "html.parser")
		reviewpage = None
		reviewpage = soup.find('a', {'class': 'eiCell cell reviews '})
		if reviewpage:
			review_page_url = 'http://glassdoor.com' + reviewpage.get('href')
			return review_page_url
		else:
			return None


	def fetch_page(self, url):
		try:
			time.sleep(2)
			self.driver.get(url)
			#while not self.driver.find_elements_by_class_name('next'):
			#	print('waiting for page to load..')

			time.sleep(2)
			self.page_source = self.driver.page_source
			return self.driver.page_source
		except TimeoutException:
			print('An error occured, Please check if url is correct.')
			exit()

	def parse_data(self,url,name):
		data = []
		soup = BS4(self.page_source, "html.parser")
		elements_divs = soup.find_all('div', {'class': 'hreview'})

		for div in elements_divs:
			date = ''
			title = ''
			rating = ''

			if div.find('time', {'class': 'date subtle small'}):
				date = div.find('time', {'class': 'date subtle small'}).get('datetime').strip()
			if (div.find('span', {'class': 'summary'})):
				title = div.find('span', {'class': 'summary'}).text.strip()
			if(div.find('span', {'class': 'value-title'})):
				rating = div.find('span', {'class': 'value-title'}).get('title').strip()

			subrating1 = ""
			subrating2 = ""
			subrating3 = ""
			subrating4 = ""
			subrating5 = ""
			
			if div.find('div', {'class': 'subRatings module'}):
				submod = div.find('div', {'class': 'subRatings module'})
			#if submod.has_attr('li'):
				for li in submod.find_all('li'):
					if 'Work/Life Balance' in li.text:
						subrating1 = li.find('span', {'class': 'gdBars gdRatings med '}).get('title').strip()
				
					elif 'Culture & Values' in li.text:
						subrating2 = li.find('span', {'class': 'gdBars gdRatings med '}).get('title').strip()
				
					elif 'Career Opportunities' in li.text:
						subrating3 = li.find('span', {'class': 'gdBars gdRatings med '}).get('title').strip()
				
					elif 'Comp & Benefits' in li.text:
						subrating4 = li.find('span', {'class': 'gdBars gdRatings med '}).get('title').strip()
				
					elif 'Senior Management' in li.text:
						subrating5 = li.find('span', {'class': 'gdBars gdRatings med '}).get('title').strip()
			
			
			
			valid = ''
			if (div.find('span', {'class': 'authorJobTitle'}))
				valid = div.find('span', {'class': 'authorJobTitle'}).text.strip()
			if(valid):
				status=valid.split("-")[0]
				position =valid.split("-")[1]
			else:
				status=position=''
			location = ''
			if(div.find('span', {'class': 'authorLocation'})):
				valid = div.find('span', {'class': 'authorLocation'}).text.strip()
				location = valid
			else:
				location = 'invalid location'

			count = '0'
			if(div.find('span', {'class': 'count'})):
				valid = div.find('span', {'class': 'count'}).text.strip()
				count = valid
			help = count.replace('(', '')

			
			element_body = div.find('div', {'class': 'cell reviewBodyCell'})

			valid = element_body.find('p', {'class': 'tightBot'})
			if valid and '(' in valid.text:
				duration = valid.text.split('(')[1]
			else:
				duration=''

			valid = element_body.find('p', {'class': ' pros mainText truncateThis wrapToggleStr'})
			pros = valid.text.strip() if valid else 'None'

			valid = element_body.find('p', {'class': ' cons mainText truncateThis wrapToggleStr'})
			cons = valid.text.strip() if valid else 'None'

			valid = element_body.find('p', {'class': ' adviceMgmt mainText truncateThis wrapToggleStr'})
			management_advice = valid.text.strip() if valid else 'None'

			outlook = {'recommends': None, 'approves': None, 'outlook': None}

			for item in element_body.find_all('div', {'class': 'middle'}):
				if 'Recommends' in item.text:
					if 'green' in item.find('i').get('class'):
						outlook['recommends'] = "1"
					elif 'yellow' in item.find('i').get('class'):
						outlook['recommends'] = "0"
					elif 'red' in item.find('i').get('class'):
						outlook['recommends'] = "-1"

				elif 'Outlook' in item.text:
					if 'green' in item.find('i').get('class'):
						outlook['outlook'] = "1"
					elif 'yellow' in item.find('i').get('class'):
						outlook['outlook'] = "0"
					elif 'red' in item.find('i').get('class'):
						outlook['outlook'] = "-1"
			review = {
				'company name': name,
				'headline': title,
				'rating': rating,
				'Work/Life Balance': subrating1,
				'Culture & Values': subrating2,
				'Career Opportunities': subrating3,
				'Comp & Benefits': subrating4,
				'Senior Management': subrating5,
				'location' : location,
				'position': position,
				'status': status,
				'date': date,
				'duration': duration,
				'cons': cons,
				'pros': pros,
				'management_advice': management_advice,
				'recommends': outlook['recommends'],
				'outlook': outlook['outlook'],
				'helpful':help,
				'url' : url
			}

			data.append(review)

		return data

	def fetch_nextpage(self):
		time.sleep(4)
		soup = BS4(self.page_source, "html.parser")
		findpage = soup.find('li', {'class': 'next'})
		if findpage:
			if findpage.find('a'):
				nextpage_url = 'http://glassdoor.com' + findpage.find('a').get('href')
				return nextpage_url
		else:
			return None
