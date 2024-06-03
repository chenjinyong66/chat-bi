"""
本地知识库配置
"""
import streamlit as st
import openai
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.chat_engine.types import ChatMode

from llms.LLMs import openai_llm

try:
    from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader, Settings
except ImportError:
    from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader, Settings

st.set_page_config(page_title="Agent智能体应用系统实战", page_icon="🦙", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)
openai.api_key = st.secrets.openai_key
openai.base_url = st.secrets.base_url
llm = openai_llm(temperature=0.7,
                 system_prompt="你是Streamlit Python库的专家，你的工作是回答技术问题。假设所有问题都与Streamlit "
                               "Python库有关。请确保你的答案具有技术性并基于事实——不要臆造功能。")
Settings.llm = llm

st.title("与Streamlit文档进行聊天 💬🦙")
st.info("课程咨询及资料获取微信：huice666", icon="📃")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        ChatMessage(role=MessageRole.ASSISTANT, content="向我提问有关Streamlit开源Python库的问题吧！")
    ]


@st.cache_resource(show_spinner=True)
def load_data():
    with st.spinner(text="正在加载和索引文档 - 请稍候！大约需要1-2分钟......"):
        reader = SimpleDirectoryReader(input_dir="data", recursive=True)
        docs = reader.load_data()
        temp_index = VectorStoreIndex.from_documents(docs)
        return temp_index


index = load_data()

if "chat_engine" not in st.session_state.keys():  # 初始化聊天引擎
    st.session_state.chat_engine = index.as_chat_engine(chat_mode=ChatMode.CONTEXT, verbose=True)

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
            text = st.write_stream(response.response_gen)

            chatMessage = ChatMessage(role=MessageRole.ASSISTANT, content=text)
            st.session_state.messages.append(chatMessage)  # 添加响应到消息历史记录
