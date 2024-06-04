import customer_tools
import streamlit as st

from llama_index.core.agent import ReActAgent
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.tools import FunctionTool, QueryEngineTool, ToolMetadata

from llms.LLMs import openai_llm, moonshot_llm, deepseek_llm

try:
    from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader, Settings
except ImportError:
    from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader, Settings

st.set_page_config(page_title="Agent智能体客户服务系统", page_icon="🦙", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)
# openai.api_key = st.secrets.openai_key
# openai.base_url = st.secrets.base_url
llm = moonshot_llm()
Settings.llm = llm

st.title("与您的专属客服对话 💬🦙")
st.info("课程咨询及资料获取微信：huice666", icon="📃")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        ChatMessage(role=MessageRole.ASSISTANT, content="向我提问任何产品相关问题")
    ]


def init_tools():
    search_order_tool = FunctionTool.from_defaults(fn=customer_tools.search_order, return_direct=True)
    recommend_product_tool = FunctionTool.from_defaults(fn=customer_tools.recommend_product, return_direct=True)
    toolsList = [customer_tools.faq_query_tool(),  # 该工具是QueryEngineTool--知识库检索代码
                 recommend_product_tool,  # 该工具是FunctionTool--逻辑运算代码
                 search_order_tool,
                 ]

    return toolsList


tools = init_tools()

agent = ReActAgent.from_tools(
    tools,
    verbose=True
)
if "chat_engine" not in st.session_state.keys():  # 初始化聊天引擎

    st.session_state.chat_engine = agent

if prompt := st.chat_input("请输入您的问题"):  # 提示用户输入并将输入保存到聊天记录中
    chatMessage = ChatMessage(role=MessageRole.USER, content=prompt)

    st.session_state.messages.append(chatMessage)

for message in st.session_state.messages:  # 显示之前的聊天记录
    with st.chat_message(message.role):
        st.write(message.content)

# 如果最后一条消息不是来自助手，生成一个新的响应
if st.session_state.messages[-1].role != MessageRole.ASSISTANT:
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = st.session_state.chat_engine.stream_chat(prompt)
            print("思考的问题----%s", response)
            text = st.write_stream(response.response_gen)

            chatMessage = ChatMessage(role=MessageRole.ASSISTANT, content=text)
            st.session_state.messages.append(chatMessage)  # 添加响应到消息历史记录
