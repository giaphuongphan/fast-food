import os
import streamlit as st
import pandas as pd
import plotly.express as px
from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType


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

restaurant = st.sidebar.selectbox(label="Restaurant 👨‍🍳",
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


openai_api_key = st.sidebar.text_input(label="OpenAI API Key 🔑",
                                type="password")

st.markdown('#### 🤖 Chat with DataFrame')
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠')
if openai_api_key.startswith('sk-'):
    agent = create_pandas_dataframe_agent(
        ChatOpenAI(openai_api_key=openai_api_key, temperature=0.2, model="gpt-3.5-turbo"),
        chart_df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "Hi, how can I help you?"})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(placeholder="Ask anything about dataframe!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in agent.run(prompt):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
