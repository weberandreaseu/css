# %%
import matplotlib.pyplot as plt
import pandas as pd
from influxdb import DataFrameClient
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
# %%
client = DataFrameClient('influxdb.weberandreas.eu',
                         ssl=True,
                         verify_ssl=True,
                         port=443,
                         username='admin',
                         password='css-secret-password',
                         database='css')
df: pd.DataFrame = client.query('SELECT * FROM "orientation"')['orientation']

# %%
df.head()

# %% [markdown]

# ## Select data
# Filter testing data (not relevant for activity prediction)
features = ['alpha', 'beta', 'gamma']
df = df[~(df['label'] == 'testing')]

# test train split
test_subjects = ['68b0-c95b-eb30', '9bf6-1846-2264',  # sitting
                 'ff26-882b-dc2c', '9dfd-af56-2e0a',  # calling
                 '7ad9-d1ee-6d2a', '5332-569d-0888']  # walking
test = df[df['subject'].isin(test_subjects)]
train = df[~df['subject'].isin(test_subjects)]

# ## Train classifier
# %%
# window = pd.Timedelta('500ms')
# df.resample(window).sum()

estimator = DecisionTreeClassifier()
estimator.fit(train[features], train['label'])

# %% [markdown]

# ## Test classifier

prediction = estimator.predict(test[features])
report = classification_report(test['label'], prediction)
print(report)

