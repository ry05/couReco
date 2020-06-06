import pandas as pd 
import os

path = os.path.join("data/coursera-courses.csv")
df = pd.read_csv(path)
print(df.shape)

def split_it(x):
	return (x.split(','))

df['skills'] = df['skills'].apply(split_it)
print(df['skills'])