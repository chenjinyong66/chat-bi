"""
课程咨询微信：huice666
"""
import streamlit as st
from llama_index.core import Settings
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.chat_engine import SimpleChatEngine

from llms.LLMs import deepseek_llm, moonshot_llm, openai_llm

st.set_page_config(page_title="Agent智能体应用系统实战", page_icon="🦙", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)
st.title("Agent智能体应用系统实战 💬🦙")
st.info("课程咨询及资料获取微信：huice666", icon="📃")

llm = deepseek_llm(temperature=0.7,
                   system_prompt="你是一位人工智能助手，可以帮助用户解决各种问题，请确保你的回答准确且简洁。")
# 下面代码基本都不需要再传入大模型参数
Settings.llm = llm

if "messages" not in st.session_state.keys():  # 初始化聊天记录
    st.session_state.messages = [
        ChatMessage(role=MessageRole.ASSISTANT, content="欢迎来到但问智库平台！")
    ]

chat_engine = SimpleChatEngine.from_defaults()

if "chat_engine" not in st.session_state.keys():  # 初始化聊天引擎
    st.session_state.chat_engine = chat_engine

if prompt := st.chat_input("请输入您的问题"):  # 提示用户输入并将输入保存到聊天记录中
    chatMessage = ChatMessage(role=MessageRole.USER, content=prompt)
    # 用于界面显示用户输入及大模型返回的答案
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
