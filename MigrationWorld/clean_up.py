import zipfile
import pandas as pd
from time import sleep

with zipfile.ZipFile('PopulationWorld/data/WPP2024_Demographic_Indicators_Medium.zip','r') as zf:
    with zf.open('WPP2024_Demographic_Indicators_Medium.csv') as f:
        df = pd.read_csv(f)

# print(df.columns)
# sleep(1000)

df = df[df['ISO3_code'].notna()]
df2024 = df.loc[df['Time'] == 2024]
df = df.loc[(df['Time']<2024)]

columns = ['ISO3_code',
            'Location',
            'Time',
            'NetMigrations'
            ]

df = df[columns]
df2024 = df2024[columns]

df['Time'] = pd.to_datetime(df['Time'],format = '%Y').dt.strftime('%Y%m').astype(int)
df2024['Time'] = pd.to_datetime(df2024['Time'],format = '%Y').dt.strftime('%Y%m').astype(int)
tmp = df[columns[:3]]


for i in range(1,12):
    tmp['Time'] += 1
    df = pd.concat((df,tmp))

df = pd.concat((df,df2024))
df.sort_values(['ISO3_code','Time'], inplace=True)
df = df.reset_index().drop(columns='index')
# print(df)
df['NetMigrations'].interpolate(inplace=True)

df.to_csv('MigrationWorld/data/migration.csv',index = False)


