"""Using this to test something about docker files"""
import pandas as pd
from data_wrangling.validate import validate_data

# run the function
df = pd.read_csv('data/kisumu.csv')
print('validating data')
validate_data(df)
