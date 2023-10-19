import plotly
import plotly.graph_objs as go
import plotly.graph_objects as go
import plotly.express as px

import pandas as pd
import numpy as np
import json

class Graphs:
    def __init__(self):
        self.df = pd.read_csv("data/covid19-2021-01-21-19h03.csv", sep=";")
        self.df = self.df[self.df["sexe"] == 0]
        self.df_18 = self.df[self.df["jour"] == '2020-03-18']
        self.df_19 = self.df[self.df["jour"] == '2020-03-19']
        self.df_coor = pd.read_csv("data/cities.csv")

    def death_of_depart(self):
        data = [
            go.Bar(name='Hospital', x=self.df["dep"], y=self.df["hosp"]),
            go.Bar(name='Reanimation', x=self.df["dep"], y=self.df["rea"])
        ]
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON


    def dc_by_day(self):
        dbd = []
        df_dep = self.df[self.df["dep"] == '01']
        y = 0
        for i in df_dep["dc"]:
            if y == i:
                dbd.append(0)
            else:
                dbd.append(i-y)
                y = i
        df_dep["dbd"] = dbd
        data = [go.Scatter(x=df_dep["jour"], y=df_dep["dbd"],
                    mode='lines',
                    name='lines')]
            
        graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON

    def map(self):
        data = {'dep':[], 'lat': [], 'lng': [], 'total_death': []}
        data = pd.DataFrame(data=data)
        for i in self.df_coor["department_code"].unique():
            df_coor_by_dep = self.df_coor[self.df_coor["department_code"] == i]
            df_by_dep = self.df[self.df["dep"] == i]
            a = {'dep':i,
                'lat': df_coor_by_dep["gps_lat"].mean(),
                'lng': df_coor_by_dep["gps_lng"].mean(),
                'total_death':  df_by_dep["dc"].max()
                }
            data = data.append(a, ignore_index=True)

        data_encode = px.scatter_mapbox(data, lat="lat", lon="lng", hover_name="dep", hover_data=["total_death"],
                        color_discrete_sequence=["fuchsia"], zoom=3, height=600, mapbox_style="open-street-map")
                    
                
            
        graphJSON = json.dumps(data_encode, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON