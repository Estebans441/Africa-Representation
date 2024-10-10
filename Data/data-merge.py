import pandas as pd
import os
import pathlib

# Extract data From Banco Mundial
processed_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), 'processed')
data_save = os.path.join(pathlib.Path(__file__).parent.absolute(), 'final')

"""
DATA IMPORT
"""
africa_countries = pd.read_csv(os.path.join(processed_dir, 'africa_countries.csv'))
countries_gdp = pd.read_csv(os.path.join(data_save, 'countries_gdp.csv'))
economic_outlook = pd.read_csv(os.path.join(data_save, 'economic_outlook.csv'))
hdr_data = pd.read_csv(os.path.join(data_save, 'hdr_data.csv'))


"""
DATA MERGING
"""
# Merge africa_countries with economic_outlook on Country Code withouth africa countries Country Name column
africa_countries.drop(columns=['Country Name'], inplace=True)
africa_countries = africa_countries.merge(economic_outlook, on='Country Code', how='left')

# Drop duplicates
africa_countries.drop_duplicates(subset=['Country Code'], inplace=True)

# Drop nan Country name rows
africa_countries.dropna(subset=['Country Name'], inplace=True)

# Merge africa_countries with countries_gdp on Country Name
africa_countries = africa_countries.merge(countries_gdp, on='Country Name', how='left')

# Order columns (first Country Name and Country Code) and sort the others alphabetically
columns = ['Country Name', 'Country Code'] + sorted([col for col in africa_countries.columns if col not in ['Country Name', 'Country Code']])
africa_countries = africa_countries[columns]

# Save the result to a CSV file
africa_countries.to_csv(os.path.join(data_save, 'africa_countries.csv'), index=False)

