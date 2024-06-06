from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool

model = ChatOpenAI(openai_api_key="sk-149bf3c0b0e543609274d93ffec44824", openai_api_base="https://api.deepseek.com/v1",
                   model_name="deepseek-chat")


@tool
def magic_function(input: int) -> int:
    """Applies a magic function to an input."""
    return input + 2

print(magic_function.name)
print(magic_function.description)


class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")


@tool("search-tool", args_schema=SearchInput, return_direct=True)
def search(query: str) -> str:
    """Look up things online."""
    return query+"==hi we LangChain"

tools = [magic_function,search]
# magic_tool = FunctionTool.from_defaults(magic_function)

# 创建包含 BaseTool 类型元素的序列


query = "what is the value of magic function 3 ?"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)

from langchain.agents import create_openai_functions_agent

# agent = create_openai_functions_agent(model, tools, prompt)

from langchain.agents import AgentExecutor

from langchain.agents import create_openai_functions_agent
agent = create_openai_functions_agent(model, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "hi"})

# agent = create_tool_calling_agent(model, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
#
# invoke = agent_executor.invoke({"input": query})
# print(invoke)
