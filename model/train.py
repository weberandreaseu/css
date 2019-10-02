# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from influxdb import DataFrameClient
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from sklearn_porter import Porter
from sklearn.model_selection import GroupKFold
# %%
client = DataFrameClient('influxdb.weberandreas.eu',
                         ssl=True,
                         verify_ssl=True,
                         port=443,
                         username='admin',
                         password='css-secret-password',
                         database='css')
raw_data: pd.DataFrame = client.query(
    'SELECT * FROM "orientation"')['orientation']

# %%
raw_data.head()

# %% [markdown]

# ## Data preparation
# Aggregate time series in window and calculate mean and variance
features = ['alpha', 'beta', 'gamma']
features_agg = [f + '_mean' for f in features] + [f + '_var' for f in features]


def mean_and_variance(frame: pd.DataFrame) -> pd.DataFrame:
    mean = frame.mean()
    variance = frame.var()
    return pd.concat([mean, variance])


def resample_dataset(df: pd.DataFrame, freq='1s') -> pd.DataFrame:
    # resample to given frequency and aggragate to mean and variance of time window
    grouper = df.groupby(['subject', pd.Grouper(freq=freq)])
    resampled = grouper[features].apply(mean_and_variance)
    # update columns names
    resampled.columns = features_agg
    # get subject labels and  merge them with resampled dataset
    labels = df.drop_duplicates('subject').set_index('subject')['label']
    return resampled.merge(labels, on='subject').set_index(resampled.index)

# some measurments may contain nan because of few data for variance
# drop them
agg_data = resample_dataset(raw_data).dropna()


# %% [markdown]

# ## Select data
# Filter testing data (not relevant for activity prediction)
agg_data = agg_data[~(agg_data['label'] == 'testing')]


def grouped_test_train_split(x, y, groups, test_size=0.3):
    """Splits dataset into test and train data without splitting groups"""
    unique_groups = np.unique(groups)
    n_test = max(int(len(unique_groups) * test_size), 1)
    selected_groups = np.random.choice(unique_groups, n_test)
    split_mask = np.in1d(groups, selected_groups)
    x_train = x[split_mask, :]
    y_train = y[split_mask]
    x_test = x[~split_mask, :]
    y_test = y[~split_mask]
    return x_train, x_test, y_train, y_test


# test train split
groups = agg_data.index.get_level_values(0).values
x_train, x_test, y_train, y_test = grouped_test_train_split(
    agg_data[features_agg].values,
    agg_data['label'].values,
    groups)



# ## Train classifier
# %%

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
    estimator.fit(x_train, y_train)
    y_pred = estimator.predict(x_test)
    model_scores = {name: metric(y_test, y_pred, average='weighted')
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
estimator.fit(x_train, y_train)
y_pred = estimator.predict(x_test)
report = classification_report(y_test, y_pred)  # , output_dict=True)
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
