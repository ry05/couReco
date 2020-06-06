"""
Purpose: To scrape data from Coursera's Website
Links Used: 
	https://realpython.com/beautiful-soup-web-scraper-python/
	https://medium.com/analytics-vidhya/web-scraping-and-coursera-8db6af45d83f
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
	
# Explore the Website
# Link: https://www.coursera.org/courses
# Base URL: https://www.coursera.org/courses
# Query Parameters: ?page=1&index=prod_all_products_term_optimization
# Page Number Range: 1-100

class DataMaker:
	"""
	Creates the data by scraping the website
	"""

	site_url = None
	first_page = None
	last_page = None
	urls = []
	courses = []
	organizations = []
	learning_products = []
	ratings = []
	num_rated = []
	difficulty = []
	enrolled = []

	def __init__(self, site, first_page, last_page):
		"""
		Initialises the page limit within
		which the data is to be scraped
		"""

		self.site_url = site
		self.first_page = first_page
		self.last_page = last_page

	def scrape_features(self, page_url):
		"""
		Scrapes 8 features from each page
		-----
		page_url:
			URL of the page
		"""

		# create the soup with a certain page URL
		course_list_page = requests.get(page_url)
		course_list_soup = BeautifulSoup(course_list_page.content,
										'html.parser')

		# pick course name
		cnames = course_list_soup.select(".headline-1-text")
		for i in range(10):
			self.courses.append(cnames[i].text)

		# pick partner name
		pnames = course_list_soup.select(".horizontal-box > .partner-name")
		for i in range(10):
			self.organizations.append(pnames[i].text)

		# pick URLs
		root = "https://www.coursera.org"
		links = course_list_soup.select(
			".ais-InfiniteHits > .ais-InfiniteHits-list > .ais-InfiniteHits-item" 
		)
		for i in range(10):
			self.urls.append(root+links[i].a["href"])

		# pick learning product
		for i in range(10):
			learn_pdcts = course_list_soup.find_all('div', '_jen3vs _1d8rgfy3')
			self.learning_products.append(learn_pdcts[i].text)

		# pick course rating and number of people who rated
		ratings = []
		num_ratings = []
		cratings = course_list_soup.select(
			".ratings-text")
		cnumratings = course_list_soup.select(
			".ratings-count")
		for i in range(10):
			try:
				self.ratings.append(float(cratings[i].text))
			except:
				self.ratings.append("Missing")
			try:
				self.num_rated.append(int(cnumratings[i].text.\
					replace(',','').\
					replace('(','').\
					replace(')','')))
			except:
				self.num_rated.append("Missing")

		# pick enrollment number
		enrollers = course_list_soup.select(".enrollment-number")
		for i in range(10):
			try:
				self.enrolled.append(enrollers[i].text)
			except:
				self.enrolled.append("Missing")

		# pick difficulty
		difficulty = course_list_soup.select(".difficulty")
		for i in range(10):
			self.difficulty.append(difficulty[i].text)

	def crawler(self):
		"""
		Traverses between the first and last pages
		-----
		base_url:
			Base URL
		"""

		for page in range(self.first_page, self.last_page+1):
			print("\nCrawling Page " + str(page))
			page_url = self.site_url + "?page=" + str(page) +\
			           "&index=prod_all_products_term_optimization"
			
			self.scrape_features(page_url)

	def make_dataset(self):
		"""
		Make the dataset
		"""

		# initiate crawler
		self.crawler()

		data_dict = {
			"Course URL":self.urls,
			"Course Name":self.courses,
			"Learning Product Type":self.learning_products,
			"Course Provided By":self.organizations,
			"Course Rating":self.ratings,
			"Course Rated By":self.num_rated,
			"Enrolled Student Count":self.enrolled,
			"Course Difficulty":self.difficulty
		}

		data = pd.DataFrame(data_dict)

		return data
		

def main():

	dm = DataMaker("https://coursera.org/courses", 1,100)
	df = dm.make_dataset()
	destination_path = os.path.join("data/coursera-courses-overview.csv")
	df.to_csv(destination_path, index=False)

if __name__=="__main__":
	main()



