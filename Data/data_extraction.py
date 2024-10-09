import pandas as pd
import os
import pathlib

# Extract data From Banco Mundial
data_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), 'raw')
processed_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), 'processed')
data_save = os.path.join(pathlib.Path(__file__).parent.absolute(), 'final')

"""
Banco mundial data
"""
# Data from https://datos.bancomundial.org/indicador/SP.POP.TOTL?locations=A9
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
countries_population['Average Population'] = countries_population[['2018', '2019', '2020', '2021', '2022']].mean(axis=1)

# Drop rows with country name and region as NaN
countries_metadata.dropna(subset=['Country Name'], inplace=True)
countries_metadata.dropna(subset=['Region'], inplace=True)

# Select countries with region containing África
africa_countries = countries_metadata[countries_metadata['Region'].str.contains('África')]

# Rename column income group
africa_countries = africa_countries.rename(columns={'Income_Group': 'Income group'})
countries_population = countries_population.rename(columns={'2022' : 'Population 2022'})

# Select relevant columns
africa_countries = africa_countries[['Country Name', 'Country Code', 'Income group', 'Region']]
countries_population = countries_population[['Country Code', 'Population 2022', 'Average Population']]

# Merge with population data
africa_countries = africa_countries.merge(countries_population, on='Country Code', how='left')
africa_countries = africa_countries.sort_values('Country Name')

# Save the result to a CSV file
africa_countries.to_csv(os.path.join(processed_dir, 'africa_countries.csv'), index=False)

"""
Data Africa
"""
# Data from https://www.kaggle.com/datasets/ivanbyone/population-and-gdp-africa
countries_gdp = pd.read_csv(os.path.join(data_dir, 'Data_Africa.csv'))

# Strip extra spaces from column names
countries_gdp.columns = countries_gdp.columns.str.strip()

# Pivot the DataFrame to have 'Year' as columns and 'Population' and 'GDP (USD)' as values
countries_gdp = countries_gdp.pivot(
    index=['Country', 'Continent'], 
    columns='Year',
    values=['Population', 'GDP (USD)']
)

# Flatten the column names for easier access
countries_gdp.columns = [f'{col[0]}_{col[1]}' for col in countries_gdp.columns]
countries_gdp = countries_gdp.reset_index()

# Create columns with the average population and GDP over the last 5 years
years = ['2018', '2019', '2020', '2021', '2022']
population_columns = [f'Population_{year}' for year in years]
gdp_columns = [f'GDP (USD)_{year}' for year in years]

countries_gdp['Average Population'] = countries_gdp[population_columns].mean(axis=1)
countries_gdp['Average GDP (USD)'] = countries_gdp[gdp_columns].mean(axis=1)

# Select the relevant columns
countries_gdp = countries_gdp[['Country', 'Continent', 'Average Population', 'Average GDP (USD)']]

# Save the result to a CSV file
countries_gdp.to_csv(os.path.join(processed_dir, 'countries_gdp.csv'), index=False)

"""
Economic outlook
"""
# https://www.kaggle.com/datasets/waalbannyantudre/african-economic-outlook
# Download URL:,http://dataportal.opendataforafrica.org/mhuiccf/african-economic-outlook-january-2019
# Source: African Development Bank

economic_outlook = pd.read_csv(os.path.join(data_dir, 'african-economic-outlook.csv'))

# Define years and extract unique indicators
years = ['2016', '2017', '2018', '2019', '2020']
economic_indicators = economic_outlook['Indicators Name'].unique()

# Pivot the DataFrame
economic_outlook = economic_outlook.pivot(
    index=['Country and Regions', 'Country and Regions Name', 'Country and Regions - RegionId'], 
    columns='Indicators Name', 
    values=years
)

# Flatten column names
economic_outlook.columns = ['_'.join(map(str, col)) for col in economic_outlook.columns]
economic_outlook = economic_outlook.reset_index()

# Create average columns for each indicator
for indicator in economic_indicators:
    indicator_columns = [f"{year}_{indicator}" for year in years]
    economic_outlook[f'Average {indicator}'] = economic_outlook[indicator_columns].mean(axis=1)

# Rename columns
economic_outlook = economic_outlook.rename(columns={'Country and Regions': 'Country Code'})
economic_outlook = economic_outlook.rename(columns={'Country and Regions Name': 'Country Name'})

# Select relevant columns
selected_columns = ['Country and Regions', 'Country and Regions Name', 'Country and Regions - RegionId'] + \
                   [f'Average {indicator}' for indicator in economic_indicators]
important_columns = [
    'Country Code', 'Country Name', 
    'Average Real GDP growth (annual %)', 'Average Real per Capita GDP Growth Rate (annual %)',
    'Average Gross domestic product, (constant prices US$)', 'Average Gross domestic product, current prices (current US$)',
    'Average Final consumption expenditure  (current US$)', 'Average Household final consumption expenditure (current US$)',
    'Average Gross capital formation (current US$)', 'Average Exports of goods and services (current US$)',
    'Average Imports of goods and services (current US$)', 'Average General government final consumption expenditure (current US$)',
    'Average Inflation, consumer prices (annual %)', 'Average Current account balance (Net, BoP, cur. US$)', 
    'Average Central government, Fiscal Balance (% of GDP)'
]
# Filter the DataFrame to select only the relevant columns
economic_outlook = economic_outlook[important_columns]

# Save the result to CSV
economic_outlook.to_csv(os.path.join(processed_dir, 'economic_outlook.csv'), index=False)

"""
DATA MERGING
"""

