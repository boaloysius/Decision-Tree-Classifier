from __init__ import *
import pandas as pd
import numpy as np
import datafilling
import plot
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans

DATA=datafilling.DATA
temp_data=datafilling.temp_data

X = temp_data.dropna()
X.is_copy = False

for col in X.columns.tolist():
	X[col]=normalize(X[col].tolist())[0]


kmeans = KMeans(n_clusters=3)
kmeans.fit(X)
centroid = kmeans.cluster_centers_
X["cluster"]=kmeans.labels_

labels=[None]*len(temp_data)
for i,index in  enumerate(X.index.tolist()):
	labels[index]=kmeans.labels_[i]

temp_data["cluster"]=pd.Series(labels)

Xone=[1 for i in range(len(X))]


plot.scatterplot(X["age"].tolist(),Xone,"age","dummy",X["cluster"].tolist())
