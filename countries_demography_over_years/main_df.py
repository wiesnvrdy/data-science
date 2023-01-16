import pandas as pd

# Read data file
src = pd.read_csv('population_international_2010_2021.csv')

# Clean unnecessary data
src.drop(['LOCATION', 'SEX', 'AGE', 'TIME', 'Flag Codes', 'Flags'], axis = 1, inplace = True)

age_raw = src.Age.unique().tolist()
src.drop(src[src.Age == age_raw[0]].index, inplace = True)
for i_age in range (age_raw.index('50 and over'), len(age_raw)):
    src.drop(src[src.Age == age_raw[i_age]].index, inplace = True)

country_raw = src.Country.unique().tolist()
for i_country in range (country_raw.index('World'), len(country_raw)):
    src.drop(src[src.Country == country_raw[i_country]].index, inplace = True)
src.drop(src[src.Sex == 'Total'].index, inplace = True)

# Preliminary grouping and formatting
src = src.groupby(['Country', 'Age', 'Time'], as_index = False).agg({'Value' : pd.Series.sum}) # 'src' is the main df
src.Value = src.Value.astype(int)
