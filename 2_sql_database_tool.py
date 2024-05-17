'''
使用QuerySQLDatabaseTool工具轻松地将查询执行添加到我们的链中
'''
from dotenv import load_dotenv
import os
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
# 但问封装的大模型调用接口
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

# db = SQLDatabase.from_uri("sqlite:///Chinook.db")

db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

# 调用但问封装的大模型对象
llm = ChatOpenAI(openai_api_key=openai_api_key, openai_api_base=openai_api_base, model_name=model_name)

generate_query = create_sql_query_chain(llm, db)
execute_query = QuerySQLDataBaseTool(db=db)

chain = generate_query | execute_query
result = chain.invoke({"question": "统计30岁以下人员的工作组和角色"})
print(result)
