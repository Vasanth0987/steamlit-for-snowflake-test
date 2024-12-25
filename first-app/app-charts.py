import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.title("Hierarchical Data Charts")

df = pd.read_csv("data/employees.csv", header=0).convert_dtypes()
st.dataframe(df)