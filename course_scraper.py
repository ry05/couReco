"""
Purpose: To scrape data from each individual course's webpage
"""

import pandas as pd 
import requests
from bs4 import BeautifulSoup
import os


class DataHunter:
	"""
	To make the big new dataset
	"""

	df = None # dataframe from scraper.py
	skills = []
	about = []
	new_career_starts = []
	pay_increase_prom = []
	estimate_toc = []
	instructors = []

	def __init__(self, df):

		self.df = df

	def scrape_features(self, page_url):
		"""
		Scrapes features from each page
		-----
		page_url:
			URL of the page
		"""

		# create the soup with a certain page URL
		course_page = requests.get(page_url)
		course_soup = BeautifulSoup(course_page.content,
										'html.parser')
		# pick course skills
		try:
			cskills = course_soup.find_all("span", "_x4x75x")
			temp = ""
			for idx in range(len(cskills)):
				temp = temp + cskills[idx].text
				if(idx != len(cskills)-1):
					temp = temp + ","
			self.skills.append(temp)
		except:
			self.skills.append("Missing")

		# pick about course
		try:
			cdescr = course_soup.select(".description")
			self.about.append(cdescr[0].text)
		except:
			self.about.append("Missing")

		# pick learner stats
		try:
			learn_stats = course_soup.select(
				"._1qfi0x77 > .LearnerOutcomes__text-wrapper > .LearnerOutcomes__percent" 
			)
		except:
			pass
		try:
			self.new_career_starts.append((float(learn_stats[0].text.replace('%',''))))
		except:
			self.new_career_starts.append("Missing")
		try:
			self.pay_increase_prom.append((float(learn_stats[1].text.replace('%',''))))
		except:
			self.pay_increase_prom.append("Missing")

		# pick estimated time to complete
		try:
			props = course_soup.select("._16ni8zai")
			done = 0 # this counter prevents duplicate values
			etoc = "Missing"
			for idx in range(len(props)):
				if('to complete' in props[idx].text and done==0):
					etoc = props[idx].text
					done+=1
			self.estimate_toc.append(etoc)
		except:
			self.estimate_toc.append("Missing")

		# pick instructors
		try:
			instructors = course_soup.select(".instructor-name")
			temp=""
			for idx in range(len(instructors)):
				temp = temp + instructors[idx].text
				if(idx != len(instructors)-1):
					temp = temp + ","
			self.instructors.append(temp)
		except:
			self.instructors.append("Missing")

	def extract_url(self):
		"""
		Extracts URLs from the dataframe loaded
		"""

		for url in self.df['Course URL']:
			self.scrape_features(url)

	def make_dataset(self):
		"""
		Make the dataset
		"""

		# initiate crawler
		self.extract_url()

		data_dict = {
				"Skills":self.skills,
				"Description":self.about,
				"Percentage of new career starts":self.new_career_starts,
				"Percentage of pay increase or promotion":self.pay_increase_prom,
				"Estimated Time to Complete":self.estimate_toc,
				"Instructors":self.instructors
			}

		data = pd.DataFrame(data_dict)

		return data

def main():

	source_path = os.path.join("data/coursera-courses-overview.csv")
	df = pd.read_csv(source_path)
	dh = DataHunter(df)
	df = dh.make_dataset()
	destination_path = os.path.join("data/coursera-individual-courses.csv")
	df.to_csv(destination_path, index=False)

if __name__=="__main__":
	main()