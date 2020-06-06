"""
Prepares Data for Analysis
	- Aggregates the two files
	- Performs preliminary pre-processing
"""

import pandas as pd 
import numpy as np
import os

def clean_col_names(df, columns):
	"""
	Cleans column names
	-----
	columns:
		List of column names
	"""

	new = []
	for c in columns:
		new.append(c.lower().replace(' ','_'))
	return new

def prepare_data(df):
	"""
	Prepares the final dataset
	-----
	df:
		dataframe
	"""

	# clean column names
	df.columns = clean_col_names(df, df.columns)

	# impute missing values that creeped in
	df['skills'] = df['skills'].fillna('Missing')
	df['instructors'] = df['instructors'].fillna('Missing')

	# making certain features numeric
	def make_numeric(x):
		if(x=='Missing'):
			return np.nan
		return float(x)

	df['course_rating'] = df['course_rating'].apply(make_numeric)
	df['course_rated_by'] = df['course_rated_by'].apply(make_numeric)
	df['percentage_of_new_career_starts'] = df['percentage_of_new_career_starts'].apply(make_numeric)
	df['percentage_of_pay_increase_or_promotion'] = df['percentage_of_pay_increase_or_promotion'].apply(make_numeric)

	def make_count_numeric(x):
	    if('k' in x):
	        return (float(x.replace('k','')) * 1000)
	    elif('m' in x):
	        return (float(x.replace('m','')) * 1000000)
	    elif('Missing' in x):
	        return (np.nan)

	df['enrolled_student_count'] = df['enrolled_student_count'].apply(make_count_numeric)

    # extract time to complete
	def find_time(x):
	    l = x.split(' ')
	    idx = 0
	    for i in range(len(l)):
	        if(l[i].isdigit()):
	            idx = i 
	    try:
	        return (l[idx] + ' ' + l[idx+1])
	    except:
	        return l[idx]

	df['estimated_time_to_complete'] = df['estimated_time_to_complete'].apply(find_time)

	def split_it(x):
		return (x.split(','))

	df['skills'] = df['skills'].apply(split_it)
	df['instructors'] = df['instructors'].apply(split_it)

	# store data
	# store it back to /data as preprocessed data
	destination_path = os.path.join("data/coursera-courses.csv")
	df.to_csv(destination_path, index=False)

def main():

	source_path1 = os.path.join("data/coursera-courses-overview.csv")
	source_path2 = os.path.join("data/coursera-individual-courses.csv")
	df_overview = pd.read_csv(source_path1)
	df_individual = pd.read_csv(source_path2)
	df = pd.concat([df_overview, df_individual], axis=1)

	# preprocess it now
	prepare_data(df)

if __name__=="__main__":
	main()