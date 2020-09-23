import numpy as np
import pandas as pd
from helpers.dbHelper import MongodbInteracter
import plotly.offline as pyo
import plotly.graph_objs as go
import datetime

class DataVisualizer:
    def visualizer(self):
        dbHandle = MongodbInteracter(dbName='tsa', collectionName='twitter')
        tweets = dbHandle.fetchContents()
        df = pd.DataFrame(tweets)
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


        df2 = pd.DataFrame(
                dataframeList.tolist(),
                columns=["positive", "negative", "neutral"])
        df2['created_at'] = df.created_at.unique()
        
        data = pd.pivot_table(df2, values = ['positive','negative','neutral'], index='created_at')
        data.head()
        # Create traces
        trace0 = go.Bar(
            x = data.index,
            y = data.positive,
            name = 'positive'
        )
        trace1 = go.Bar(
            x = data.index,
            y = data.negative,
            name = 'negative'
        )
        trace2 = go.Bar(
            x = data.index,
            y = data.neutral,
            name = 'neutral'
        )

        data = [trace0,trace1,trace2]
        # layout = go.Layout(title = 'Positive vs Negative vs Neutral')
        figure = go.Figure(data=data)
        return pyo.plot(figure)
    

 