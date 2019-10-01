#%%
from influxdb import DataFrameClient
import pandas as pd
import matplotlib.pyplot as plt

# %%
client = DataFrameClient('influxdb.weberandreas.eu',
                        ssl=True,
                        verify_ssl=True,
                        port=443,
                        username='admin',
                        password='css-secret-password',
                        database='css')
df: pd.DataFrame = client.query('SELECT * FROM "orientation"')['orientation']

#%%
df.head()
#%%
df.label.value_counts().plot.barh()
plt.ylabel('activity')
plt.xlabel('# measurements')
plt.show()
#%%
unique_subjects = df.drop_duplicates('subject')
unique_subjects.groupby('label').count().subject.plot.barh()
plt.ylabel('activity')
plt.xlabel('# subjects')
plt.show()