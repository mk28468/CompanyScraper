workflow:

0. python 2.7 environment; selenium, BeautifulSoup(bs4) packages are needed to run this program

0.5. chromedriver needs to be in the same directory 

1. fill in glassdoor company review url and desired output file name in Web_Scrapper.py
	-review page needs to be under company/review; sample review page: https://www.glassdoor.com/Reviews/RenaissanceRe-Reviews-E4444.htm

2. fill in glassdoor username and password in WBClass.py (you only need to do this once during setup)

3. to run: python Web_Scrapper.py


Troubleshooting: 
to fix python path: windows system advanced system settings, system path: add ;\c:\python27 and ...\scripts
make sure you are using the 64bit python version

to install selenium and bs4:
 	pip install selenium
 	pip install bs4