import numpy as np
import pandas as pd


# In[2]:


import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np
import datetime as dt
from pymongo import MongoClient

uri = "mongodb://tsaUser:tsa%40123@192.168.50.125/?authSource=tsa&authMechanism=SCRAM-SHA-256"
connection = MongoClient(uri)
db = connection['tsa']
col=db['twitter']
df = pd.DataFrame(list(col.find()))
df.head()

df['created_at'] = pd.to_datetime(df['created_at'])
df['created_at'] = df.created_at.map(lambda x: x.strftime('%Y-%m-%d'))
df['wo_split'] = df['classification'].apply(lambda x: x.get('wo_split'))
df['wo_split'] = df['wo_split'].apply(lambda x: x.get('result'))


dataframeList = [(df.groupby('created_at').wo_split.apply(lambda x: (x=='pos').sum())).reset_index().wo_split.values.tolist(),
        (df.groupby('created_at').wo_split.apply(lambda x: (x=='neg').sum())).reset_index().wo_split.values.tolist(),
        (df.groupby('created_at').wo_split.apply(lambda x: (x=='neutral').sum())).reset_index().wo_split.values.tolist()]

dataframeList = np.asarray(dataframeList)
dataframeList = dataframeList.transpose()


df4 = pd.DataFrame(
                dataframeList.tolist(),
                columns=["positive", "negative", "neutral"])
df4['created_at'] = df.created_at.unique()
        
data1 = pd.pivot_table(df4, values = ['positive','negative','neutral'], index='created_at')
data1.head()
# Create traces
trace0 = go.Bar(
            x = data1.index,
            y = data1.positive,
            name = 'positive'
        )
trace1 = go.Bar(
            x = data1.index,
            y = data1.negative,
            name = 'negative'
        )
trace2 = go.Bar(
            x = data1.index,
            y = data1.neutral,
            name = 'neutral'
        )

data4 = [trace0,trace1,trace2]
# layout = go.Layout(title = 'Positive vs Negative vs Neutral')
figure = go.Figure(data=data4)
pyo.plot(figure)


# In[ ]:





# In[ ]:





# In[ ]:




