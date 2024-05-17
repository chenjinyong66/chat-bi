from dotenv import load_dotenv
import os

from langchain.agents import AgentType
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI


load_dotenv()
os.environ.pop('LANGCHAIN_TRACING_V2', None)

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
openai_api_key = os.getenv('OPENAI_API_KEY')
model_name = os.getenv('MODEL_NAME')
openai_api_base = os.getenv('OPENAI_API_BASE')

db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# 调用但问封装的大模型对象
llm = ChatOpenAI(openai_api_key=openai_api_key, openai_api_base=openai_api_base, model_name=model_name)

agent_executor = create_sql_agent(llm, db=db, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
agent_executor.invoke({"input": "统计每个校色下的人员数量"})

# agent_executor.invoke({"input": "统计30岁以下人员的工作组和角色"})
# agent_executor.invoke({"input": "统计每个工作组下的人员数量"})
