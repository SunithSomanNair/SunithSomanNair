import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pyodbc
import numpy as np
pio.templates.default = "plotly_white"

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=SUNITH;'
                      'Database=COPDB;'
                      'Trusted_Connection=yes;'
                      'autocommit=True;')

cursor = conn.cursor()
cursor.execute("select * from rides where (RidesCompleted is  not null) and (cast(RidesCompleted as decimal)/cast(RidersActivePerHour as decimal) * 100) >= 40")

DriversActivePerHour = []
RidersActivePerHour = []
RidesCompleted = []
SupplyRatio = []
for i in cursor:
    DriversActivePerHour.append(i[0])
    RidersActivePerHour.append(i[1])
    RidesCompleted.append(i[2])
    SupplyRatio.append(i[2]/i[0])

demand = RidersActivePerHour
supply = DriversActivePerHour

#Scatter plot for supply and demand
figure = px.scatter(x = DriversActivePerHour, y = RidersActivePerHour, trendline="ols", title="Demand and Supply Analysis")
figure.update_layout(xaxis_title="Number of Drivers Active per Hour (Supply)", yaxis_title="Number of Riders Active per Hour (Demand)")
figure.show()

#Calculate elasticity
pct_change_demand = (np.max(demand) - np.min(demand)) / np.mean(demand) * 100
pct_change_supply = (np.max(supply) - np.min(supply)) / np.mean(supply) * 100
elasticity = pct_change_demand / pct_change_supply
print("Elasticity of demand with respect to the number of active drivers per hour: {:.2f}".format(elasticity))

#Calculate the supply ratio for each level of driver activity
fig = go.Figure()
fig.add_trace(go.Scatter(x = DriversActivePerHour, y = SupplyRatio, mode='markers'))
fig.update_layout(title='Supply Ratio vs. Driver Activity', xaxis_title='Driver Activity (Drivers Active Per Hour)', yaxis_title='Supply Ratio (Rides Completed per Driver Active per Hour)')
fig.show()