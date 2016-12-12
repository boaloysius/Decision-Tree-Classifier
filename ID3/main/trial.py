from __init__ import *
from dataFormating.DataRetrival import *
data1=DataRetrival(file="database/mixed/train_mixed.csv")
df= pd.DataFrame(index=data1.columns)
print df