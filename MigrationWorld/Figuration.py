import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('MigrationWorld/data/migration.csv')
# print(df.head(5))
time = 200001
largest_migration = df.loc[(df['Time']==time)].nlargest(10,columns='NetMigrations').sort_values('NetMigrations',ascending=True)
smallest_migration = df.loc[(df['Time']==time)].nsmallest(10,columns='NetMigrations').sort_values('NetMigrations', ascending=True)
print(largest_migration)
print(smallest_migration)
migration_mix = pd.concat([smallest_migration,largest_migration])
plt.barh(migration_mix['Location'],
         migration_mix['NetMigrations'])

plt.tight_layout()
plt.show()
