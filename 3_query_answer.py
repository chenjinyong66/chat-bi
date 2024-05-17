'''
将原始问题和SQL查询结果结合起来生成最终答案
'''
from dotenv import load_dotenv
import os
from operator import itemgetter

from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
os.environ.pop('LANGCHAIN_TRACING_V2', None)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """
)

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

answer = answer_prompt | llm | StrOutputParser()
chain = (
        RunnablePassthrough.assign(query=generate_query).assign(
            result=itemgetter("query") | execute_query
        )
        | answer
)

response = chain.invoke({"question": "统计每个工作组下的人员数量？"})
print(response)
