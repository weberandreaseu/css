# %%
import matplotlib.pyplot as plt
import pandas as pd
from influxdb import DataFrameClient
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from sklearn_porter import Porter
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

estimators = {
    'dummy': DummyClassifier(),
    'decision_tree': DecisionTreeClassifier(),
    'svc': SVC(),
    'random_forest': RandomForestClassifier()
}
metrics = {
    # 'accuracy': accuracy_score,
    'precesion': precision_score,
    'recall': recall_score
    # 'f1': f1_score
}
scores = pd.DataFrame(columns=metrics.keys())

for estimator_name, estimator in estimators.items():
    estimator.fit(train[features], train['label'])
    y_true = test['label'].ravel()
    y_pred = estimator.predict(test[features])
    model_scores = {name: metric(y_true, y_pred, average='weighted')
                    for name, metric in metrics.items()}
    model_scores['estimator'] = estimator_name
    scores = scores.append(model_scores, ignore_index=True)
scores.set_index('estimator')
# %%
scores.plot.bar(x='estimator', rot=20)
plt.show()

# %% [markdown]

# ## Test classifier
estimator = DecisionTreeClassifier()
estimator.fit(train[features], train['label'])
prediction = estimator.predict(test[features])
report = classification_report(test['label'], prediction) #, output_dict=True)
print(report)
# report = pd.DataFrame(report)
# report['estimator'] = 'decision_tree'


# %% [markdown]

# ## Export model
# Use sklearn porter to export trained model to java script.

porter = Porter(estimator, language='js')
output = porter.export(embed_data=True)
with open('model.js', 'w') as file:
    file.write(output)