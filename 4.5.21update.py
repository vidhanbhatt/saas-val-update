import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from matplotlib import dates
import altair as alt
from PIL import Image


df = pd.read_csv("st_valupdate_test.csv")

st.title("EV/Run-Rate Revenue Multiple by Day")
groups = st.multiselect(
    "Choose Stock or Index from Dropdown", df.columns.tolist(), ["Date","All SaaS","High Growth SaaS","Low Growth SaaS"
]
)

d1 = st.date_input(
    "Choose Start Date",
    datetime.date(2020, 3, 2))

d2 = st.date_input(
    "Choose End Date",
    datetime.date(2021, 4, 5))

start=  np.busday_count(datetime.date(2020,3,2),d1)-3
end =  np.busday_count(datetime.date(2020,3,2),d2)-1

data = df.loc[start:end,groups]
data = data.melt("Date",var_name="group", value_name="multiple")

x= alt.Chart(data).mark_line(point=False).encode(
    x=alt.X("Date"),
    y=alt.Y('multiple',axis=alt.Axis(title="multiple"),scale=alt.Scale(domain=(0, 70))),
    color=alt.Color('group',legend=alt.Legend(title="Stock"))
).properties(
    width=1200,
    height=450
)

text=x.mark_text(
    align='left',
    dx=1,
    dy=-10,
).encode(
    text="multiple",
)

check = st.checkbox("show values")

if check:
    st.write(x+text)
else:
    st.write(x) 

dfi=pd.read_csv("recent_ipos_v2.csv")

dfi = dfi.melt("Company",var_name="metric", value_name="value")

st.title("Recent Ipos/S1s")
z = alt.Chart(dfi).mark_bar().encode(
    x='Company',
    y='value',
    color='Company',
).properties(
    width=150,
    height=300
)

textz=z.mark_text(
    align='center',
    baseline='bottom',
    dx=0,
    dy=-20
).encode(
    text="value"
)

show = alt.layer(z,textz,data=dfi).facet(column="metric")
st.write(show)
