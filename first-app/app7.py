import urllib.parse, uuid
import pandas as pd
import streamlit as st
from io import StringIO

def getGraph(df):
    edges = ""
    for _, row in df.iterrows():
        if not pd.isna(row.iloc[1]):
            edges += f'\t"{row.iloc[0]}" -> "{row.iloc[1]}";\n'
    return f'digraph {{\n{edges}}}'


def OnShowList(filename):
    if "names" in st.session_state:
        filenames = st.session_state["names"]
        if filename in filenames:
            st.error("Critical file found!")
            st.stop()


def getSessionId():
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
    return st.session_state["session_id"]

@st.cache_data(show_spinner="Loading the csv file...")
def loadfile(SessionId, filename):
    return pd.read_csv(filename, header=0).convert_dtypes()


st.title("Hierarchical Data Viewer")

if "names" in st.session_state:
    filenames = st.session_state["names"]
else:
    filenames = ["data/employees.csv"]
    st.session_state["names"] = filenames

filename ="data/employees.csv"
uploaded_file = st.sidebar.file_uploader(
    "upload a CSV file", type = ["csv"], accept_multiple_files=False
)
if uploaded_file is not None:
    filename = StringIO(uploaded_file.getvalue().decode("utf-8"))
    file = uploaded_file.name
    if file not in filenames:
        filenames.append(file)

btn = st.sidebar.button("Show List", 
                        on_click=OnShowList, args=("portfolio.csv", ))
if btn:
    for f in filenames:
        st.sidebar.write(f)

df_orig = loadfile(getSessionId(), filename)
cols = list(df_orig.columns)

with st.sidebar:
    child = st.selectbox("Child Column Name",cols,index=0)
    parent = st.selectbox("Parent Column Name",cols,index=1)
    df = df_orig[[child,parent]]
        

tabs = st.tabs(["Source","Graph","Dot Code"])
tabs[0].dataframe(df_orig)

chart = getGraph(df)
tabs[1].graphviz_chart(chart)

url = f'http://magjac.com/graphviz-visual-editor/?dot={urllib.parse.quote(chart)}'
tabs[2].link_button("Visualize Online", url)
tabs[2].code(chart)