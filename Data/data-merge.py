import pandas as pd
import os
import pathlib

# Extract data From Banco Mundial
processed_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), 'processed')
data_save = os.path.join(pathlib.Path(__file__).parent.absolute(), 'final')

"""
DATA IMPORT
"""
countries_population = pd.read_csv(os.path.join(processed_dir, 'countries_population.csv'))
economic_outlook = pd.read_csv(os.path.join(processed_dir, 'economic_outlook.csv'))
gini_index = pd.read_csv(os.path.join(processed_dir, 'gini_index.csv'))
hdr_data = pd.read_csv(os.path.join(processed_dir, 'hdr_data.csv'))


"""
DATA MERGING
"""
africa_countries = economic_outlook

# Merge the data
africa_countries = africa_countries.merge(countries_population, on='Country Code', how='left').merge(gini_index, on='Country Code', how='left').merge(hdr_data, on='Country Code', how='left')

print(africa_countries.info())

# Save the result to CSV
africa_countries.to_csv(os.path.join(data_save, 'africa_countries.csv'), index=False)