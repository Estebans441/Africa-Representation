import pandas as pd
import os
import pathlib

# Extract data From Banco Mundial
data_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), 'raw')
data_save = os.path.join(pathlib.Path(__file__).parent.absolute(), 'Database')

countries_metadata = pd.read_excel(
    os.path.join(data_dir, 'poblacion-banco-mundial.xlsx'),
    sheet_name='Metadata - Countries'
)

countries_population = pd.read_excel(
    os.path.join(data_dir, 'poblacion-banco-mundial.xlsx'),
    sheet_name='Data',
    skiprows=3
)

# Create a column with the average population
countries_population['Average Population'] = countries_population[['2019', '2020', '2021', '2022', '2023']].mean(axis=1)

# Drop rows with country name and region as NaN
countries_metadata.dropna(subset=['Country Name'], inplace=True)
countries_metadata.dropna(subset=['Region'], inplace=True)

# Select countries with region containing África
africa_countries = countries_metadata[countries_metadata['Region'].str.contains('África')]

# Rename column income group
africa_countries = africa_countries.rename(columns={'Income_Group': 'Income group'})

# Select relevant columns
africa_countries = africa_countries[['Country Name', 'Country Code', 'Income group', 'Region']]
countries_population = countries_population[['Country Code', 'Average Population']]

# Merge with population data
africa_countries = africa_countries.merge(countries_population, on='Country Code', how='left')

# Save data
africa_countries.to_csv(os.path.join(data_save, 'africa_countries.csv'), index=False)
