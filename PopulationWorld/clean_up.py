import zipfile
import pandas as pd
from time import sleep

with zipfile.ZipFile('PopulationWorld/data/WPP2024_Demographic_Indicators_Medium.zip','r') as zf:
    with zf.open('WPP2024_Demographic_Indicators_Medium.csv') as f:
        df = pd.read_csv(f)

# print(df.columns)
# sleep(1000)

countries = df[df['ISO3_code'].notna()].rename(columns={'Time':'Year', 'TPopulation1Jan':'1', 'TPopulation1July':'7'})
countries = countries[(countries['ISO3_code'].notna()) & (countries['Year']<2025)]

columns = ['ISO3_code',
            'Location',
            'Year',
            '1',
            '7']

countries['1'] = countries['1']/1000
countries['7'] = countries['7']/1000

population_df = countries[columns]

population_df = population_df.melt(id_vars=columns[:3], var_name='Month', value_name='Population')

# population_df['Year'] = population_df['Year'].astype(int)
population_df['Month'] = population_df['Month'].astype(int)

tmp = population_df[columns[:3]].drop_duplicates()

for i in range(2, 13):
    if i !=7:
        tmp['Month'] = i
        population_df = pd.concat((population_df, tmp))

population_df.sort_values(by = ['ISO3_code', 'Year', 'Month'], inplace=True)

population_df['Population'] = population_df['Population'].interpolate()
population_df.drop(population_df[(population_df['Year']==2024) & (population_df['Month']>7)].index, inplace=True)

population_df['Time'] = pd.to_datetime(population_df[['Year','Month']].assign(DAY = 1)).dt.strftime('%Y%m')
# print(population_df)


population_df.to_csv('PopulationWorld/data/popultionWorld.csv')

