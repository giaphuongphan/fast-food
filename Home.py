import os
import streamlit as st
import pandas as pd
import plotly.express as px




RESTAURANT_PATH_MAP = {
    "KFC": f"{os.getcwd()}/data/kfc_data.csv"
}


def load_dataframe(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    raise Exception(f"Invalid path {path}")


st.set_page_config(
    page_title="Fast Food Analytics",
    page_icon="🍔",
    layout="wide",
)

st.markdown(body="# 🍔 Dashboard")

restaurant = st.sidebar.selectbox(label="👨‍🍳 Restaurant",
                                  options=["KFC"])

if restaurant:
    df = load_dataframe(RESTAURANT_PATH_MAP[restaurant])
    st.markdown("#### 📈 DataFrame")
    st.data_editor(data=df, use_container_width=True)

df_cols = df.columns
chart_df = df.loc[:, df_cols]

col1, col2 = st.columns(2)
with col1:
    nutrient = st.selectbox(label="Bar chart",
                        options=df_cols[3:],
                        key="col1_box")
    st.bar_chart(data=chart_df.loc[:, ["Food", nutrient]], y=nutrient, x="Food")

with col2:
    nutrient = st.selectbox(label="Box plot",
                        options=df_cols[3:],
                        key="col2_box")

    fig = px.box(chart_df.loc[:, [nutrient]], x=nutrient, points="all")
    st.plotly_chart(fig)
