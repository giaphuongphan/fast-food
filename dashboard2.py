import os
import streamlit as st
import pandas as pd
import plotly.express as px
from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
import time
import numpy as np

# Read CSV file into a DataFrame
df_kfc = pd.read_csv('data/kfc_data.csv')
df_macs = pd.read_csv('data/macs_data.csv')

# Join 2 dataframes for comparison
combined_df = pd.concat([df_kfc, df_macs], ignore_index=True)

# Display the combined dataframe
st.markdown("#### 📈 DataFrame")
st.data_editor(data=combined_df, use_container_width=True)

df_cols_kfc = df_kfc.columns
chart_df_kfc = df_kfc.loc[:, df_cols_kfc]

st.markdown("#### 📊 KFC's Menu Items")
# display bar charts for KFC
col1, col2 = st.columns(2)
with col1:
    nutrient = st.selectbox(label="Bar chart",
                    options=df_cols_kfc[1:],
                    key="col1_box")
    st.bar_chart(data=chart_df_kfc.loc[:, ["Food", nutrient]], y=nutrient, x="Food")

# display box plots for KFC
with col2:
    nutrient = st.selectbox(label="Box plot",
                    options=df_cols_kfc[1:],
                    key="col2_box")

    fig = px.box(chart_df_kfc.loc[:, [nutrient]], x=nutrient, points="all")
    st.plotly_chart(fig)

df_cols_macs = df_macs.columns
chart_df_macs = df_macs.loc[:, df_cols_macs]

st.markdown("#### 📊 McDonald's Menu Items")
# display bar charts for Macs
col3, col4 = st.columns(2)
with col3:
    nutrient = st.selectbox(label="Bar chart",
                    options=df_cols_macs[1:],
                    key="col3_box")
    st.bar_chart(data=chart_df_macs.loc[:, ["Food", nutrient]], y=nutrient, x="Food")

# display box plots for Macs
with col4:
    nutrient = st.selectbox(label="Box plot",
                    options=df_cols_macs[1:],
                    key="col4_box")

    fig = px.box(chart_df_macs.loc[:, [nutrient]], x=nutrient, points="all")
    st.plotly_chart(fig)

st.markdown("#### ✅ Comparison")
# Selection of individual items for comparison
col5, col6 = st.columns(2)

with col5:
    first_item = st.selectbox('Select menu item #1:', combined_df['Food'])
    first_df = combined_df[combined_df['Food'] == first_item]
    first_trans_df = first_df.transpose()
    st.dataframe(first_trans_df, use_container_width=True)

with col6:
    second_item = st.selectbox('Select menu item #2:', combined_df['Food'])
    second_df = combined_df[combined_df['Food'] == second_item]
    second_trans_df = second_df.transpose()
    st.dataframe(second_trans_df, use_container_width=True)

st.markdown("#### 🥗 Daily Dietary Guidelines and Recommendations for Reference")
st.write('Recommended calorie intake based on lifestyle and age group: \nhttps://www.healthhub.sg/live-healthy/192/recommended_dietary_allowances')
st.write('Recommended protein intake (average): 76.3g (male) and 62.6g (female)')
st.write('Recommended total fat intake (average): 86.5g (male) and 67.9g (female)')
st.write('Recommended saturated fat intake (average): 28.8g (male) 22.6g (female)')
st.write('Recommended carbohydrates intake (average): 389.3g (male) and 305.7g (female)')
st.write('Recommended sodium allowance: 5000 mg')
st.write('''
        Sources: https://www.hpb.gov.sg/docs/default-source/pdf/nns-2010-report.pdf, \n
        https://www.healthhub.sg/live-healthy/15/dietary_guidelines_adults
        ''')