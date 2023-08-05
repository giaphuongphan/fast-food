from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
import pandas as pd


openai_api_key = "sk-abcdefghiklmnopqrstuvwxyz123456789"
df = pd.read_csv('data/kfc_data.csv')

agent = create_pandas_dataframe_agent(
        ChatOpenAI(openai_api_key=openai_api_key, temperature=0.2, model="gpt-3.5-turbo"),
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
    )

prompt = "How many rows are there?"
try:
    response = agent.run(prompt)
except Exception as ex:
    print(f"{str(ex)}")
