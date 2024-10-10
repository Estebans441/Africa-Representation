import pandas as pd
import os
import pathlib

# Extract data From Banco Mundial
data_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), 'raw')
processed_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), 'processed')

"""
# World bank population data
"""
# Data from https://datos.bancomundial.org/indicador/SP.POP.TOTL
countries_population = pd.read_excel(
    os.path.join(data_dir, 'world-bank-population.xlsx'),
    sheet_name='Data',
    skiprows=3
)
# Rename column income group
countries_population = countries_population.rename(columns={'2019' : 'Population 2019'})

# Select relevant columns
countries_population = countries_population[['Country Code', 'Population 2019']]

# Save the result to CSV
countries_population.to_csv(os.path.join(processed_dir, 'countries_population.csv'), index=False)

"""
# World bank Gini index data
"""
# Data from https://data.worldbank.org/indicator/SI.POV.GINI
gini_index = pd.read_excel(
    os.path.join(data_dir, 'world-bank-gini.xlsx'),
    sheet_name='Data',
    skiprows=3
)
# Rename column income group
gini_index = gini_index.rename(columns={'2019' : 'Gini Index 2019'})

# Select relevant columns
gini_index = gini_index[['Country Code', 'Gini Index 2019']]

# Save the result to CSV
gini_index.to_csv(os.path.join(processed_dir, 'gini_index.csv'), index=False)

"""
# African Economic Outlook Data
"""
economic_outlook = pd.read_csv(os.path.join(data_dir, 'african-economic-outlook.csv'))

# Define years and extract unique indicators
years = ['2019']
economic_indicators = economic_outlook['Indicators Name'].unique()

# Pivot the DataFrame
economic_outlook = economic_outlook.pivot(
    index=['Country and Regions', 'Country and Regions Name', 'Country and Regions - RegionId'], 
    columns='Indicators Name', 
    values=years
)

# Flatten column names
economic_outlook.columns = [' '.join(map(str, col[::-1])) for col in economic_outlook.columns]
economic_outlook = economic_outlook.reset_index()

# Rename columns
economic_outlook = economic_outlook.rename(columns={'Country and Regions': 'Country Code', 'Country and Regions Name': 'Country Name'})

# Filtrar las columnas necesarias
columns_to_use = [
    'Country Code', 'Country Name', 'Central government, Fiscal Balance (% of GDP) 2019', 
    'Current account balance (As % of GDP) 2019', 'Exports of goods and services (% of GDP) 2019',
    'Imports of goods and services (% of GDP) 2019', 'Inflation, consumer prices (annual %) 2019',
    'Gross capital formation (% of GDP) 2019', 'Final consumption expenditure  (% of GDP) 2019',
    'General government final consumption expenditure (% of GDP) 2019',
    'Household final consumption expenditure  (% of GDP) 2019',
    'Real GDP growth (annual %) 2019'
]

# Filtrar las columnas seleccionadas
economic_outlook = economic_outlook[columns_to_use]

# Guardar el resultado en un archivo CSV
economic_outlook.to_csv(os.path.join(processed_dir, 'economic_outlook.csv'), index=False)

"""
# Human Development Report Data
"""
hdr_data = pd.read_excel(os.path.join(data_dir, 'hdr-data.xlsx'))

# Eliminar las columnas innecesarias
hdr_data.drop(columns=['dimension', 'note'], inplace=True)

# Renombrar columnas
hdr_data = hdr_data.rename(columns={'countryIsoCode': 'Country Code'})

# Pivot the DataFrame
hdr_data = hdr_data.pivot(
    index=['Country Code'], 
    columns='indicator', 
    values='value'
)

# Flatten column names
hdr_data = hdr_data.reset_index()

# Filtrar las columnas necesarias del HDR
hdr_columns_to_use = [
    'Country Code', 'Gross National Income Per Capita (2017 PPP$)', 'Human Development Index (value)', 
    'Inequality-adjusted Human Development Index (value)', 'Life Expectancy at Birth (years)', 
    'Labour force participation rate, female (% ages 15 and older)', 
    'Labour force participation rate, male (% ages 15 and older)',
    'Maternal Mortality Ratio (deaths per 100,000 live births)', 
    'Share of seats in parliament, female (% held by women)', 
    'Expected Years of Schooling (years)'
]

# Filtrar las columnas seleccionadas
hdr_data = hdr_data[hdr_columns_to_use]

# Guardar el resultado en un archivo CSV
hdr_data.to_csv(os.path.join(processed_dir, 'hdr_data.csv'), index=False)