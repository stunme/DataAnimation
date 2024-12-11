import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('PopulationWorld/data/popultionWorld.csv')
# print(df.columns)
topCountry = df.loc[df['Time']==2024].nlargest(10,columns='TPopulation1Jan').sort_values('TPopulation1Jan',ascending=True)

plt.barh(topCountry['Location'], topCountry['TPopulation1Jan'])

plt.show()