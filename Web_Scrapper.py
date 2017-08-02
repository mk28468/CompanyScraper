import sys
from WBClass import Scrapper
import time
import csv

reload(sys)  
sys.setdefaultencoding('utf8')
"""
Read in the desired company overview url list in csv format 
"""
#url = 'https://www.glassdoor.com/Reviews/Marvell-Technology-Reviews-E11761.htm'
# ENTER THE NAME OF THE DESIRED OUTPUT FILE
overviewFilename = 'company_overview.csv'
filename = 'company_reviews.csv'


with open('./from15100.csv') as f:
	company_urls=[tuple(line) for line in csv.reader(f)]
print ('...finished loading company urls from csv file, starting web-scraper')
start = time.time()
print('logging in to Glassdoor...')
SR = Scrapper()

for companyName,overviewUrl in company_urls:
	#########################################################
	#STEP 0: test if there is no company url:
	#########################################################
	if overviewUrl == 'none':
		continue	
	#########################################################
	#STEP 1: fetch the company overview
	#########################################################
	OverviewResult = []
	print('Company name: ', companyName)
	print ('Getting overview...',overviewUrl)
	SR.fetch_overview_page(overviewUrl)
	print ('Parsing overview...',)
	overview_data = SR.parse_overview_data()
	print ('output company information')
	OverviewResult.extend(overview_data)
	print ('Writing results to %s'%overviewFilename)

	Headers = [ "Name", "Website", "Headquarters", "Size", "Founded", "Type", "Industry", "Revenue"]
	with open(overviewFilename, 'a') as f:
		headings = ','.join(Headers)
		#no need to write heading if appending overviews
		#f.write(headings+'\n')
		#f.write('\n')
		for Data in OverviewResult:
			line = ''
			for item in Headers:
				if Data[item] == None:
					Data[item] = str(Data[item])
				Data[item] = Data[item].replace(',', ' ')
				Data[item] = Data[item].replace(')', '')
				Data[item] = Data[item].replace('(', '')
				line+=Data[item]+','

			line.strip(',')
			asciiline = line.encode('ascii', 'ignore')
			f.write(asciiline+'\n')
	print ('This company overview completed')
	#########################################################
	#STEP 2: redirect to the review page from overview page
	#########################################################
	url = ''
	print('redirecting to review page of ', companyName)
	url = SR.fetch_review_page()
	print('review url is:', url)
	#########################################################
	#STEP 3: Scrapping reviews from review pages
	#########################################################
	Result = []
	print ('Starting Scrapper to {}...'.format(url.split('.')[1]))
	print ('Getting reviews page 1...')
	SR.fetch_page(url)
	print ('parsing...',)
	data = SR.parse_data(url,companyName)
	print (len(data), 'reviews found on this page.')
	Result.extend(data)

	count = 2
	Next_Page = True
	while Next_Page:
		Next_Page = SR.fetch_nextpage()
		if Next_Page:
			print ('Getting reviews page %s...'%(count))
			SR.fetch_page(Next_Page)
			print ('parsing...')
			data = SR.parse_data(Next_Page,companyName)
			print (len(data), 'reviews found on this page.')
			Result.extend(data)
			count +=1

		#for now only getting the first 5 pages to save time
		#if count > 2:
		#	Next_Page = False

	print ('Writing results to %s'%filename)
	Headers = [ "company name","headline", "rating", "Work/Life Balance", "Culture & Values", "Career Opportunities", "Comp & Benefits", "Senior Management", "location", "position", "status", "date", "duration", "cons", "pros", "management_advice",
				"recommends", "outlook", "helpful", "url" ]
	with open(filename, 'a') as f:
		headings = ','.join(Headers)
		#f.write(headings+'\n')
		#let's not writing headings for this one since we are getting all reviews together
		for Data in Result:
			line = ''
			for item in Headers:
				if Data[item] == None:
					Data[item] = str(Data[item])
				Data[item] = Data[item].replace(',', ' ')
				Data[item] = Data[item].replace(')', '')
				Data[item] = Data[item].replace('(', '')
				#print ("data is ",Data[item])
				#temp = Data[item].encode('ascii', 'ignore')
				temp = unicode(Data[item])
				#print ("temp is ",temp)
				line+=temp+','
				
				#line+=Data[item]+','
			
			line.strip(',')
			#asciiline = line.encode('ascii', 'ignore')
			#f.write(asciiline+'\n')
			f.write(line+'\n')
	print('This company complete! Switching to the next company...')
	
print ('Total time: ' + str((time.time()-start)/60).format("%2f") + 'minutes')
print ('Completed Successfully, Exiting...')










