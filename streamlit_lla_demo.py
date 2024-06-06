from pathlib import Path

import streamlit as st
from llama_index.core.agent import ReActAgent
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.core.tools import FunctionTool

import customer_tools
from tools.ssh import ssh
from tools.ipInfo import ipinfo
from tools.python_exec import execute_python

from file_tools import FileTools
from llms.LLMs import moonshot_llm, deepseek_llm
from ops_agent.hdfs_analyse.hdfscluster import HDFSCluster

try:
    from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader, Settings
except ImportError:
    from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader, Settings

st.set_page_config(page_title="Agent智能体客户服务系统", page_icon="🦙", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)

llm = deepseek_llm()
Settings.llm = llm

st.title("与您的专属客服对话 💬🦙")
st.info("更多精彩实战，关注知徒学AI", icon="📃")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        ChatMessage(role=MessageRole.ASSISTANT, content="向我提问任何hdfs集群相关问题")
    ]

file_tool = FileTools(Path.cwd())
hdfs_tool = HDFSCluster("10.212.1.67")


def init_tools():
    # 创建一个保存文件的工具，该工具对应的函数是FileTools类中的save_file函数
    save_file_tool = FunctionTool.from_defaults(fn=file_tool.save_file)
    read_file_tool = FunctionTool.from_defaults(fn=file_tool.read_file)
    list_files_tool = FunctionTool.from_defaults(fn=file_tool.list_files)
    hdfs_log_tool = FunctionTool.from_defaults(fn=hdfs_tool.namenode_log)
    hdfs_touch_tool = FunctionTool.from_defaults(fn=hdfs_tool.hdfs_touchz)
    hdfs_nodes_tool = FunctionTool.from_defaults(fn=hdfs_tool.get_namenodes)
    hdfs_exec_tool = FunctionTool.from_defaults(fn=hdfs_tool.exec_command)
    hdfs_disk_free_tool = FunctionTool.from_defaults(fn=hdfs_tool.get_local_disk_free)
    ipinfo_tool = FunctionTool.from_defaults(fn=ipinfo)
    execute_python_tool = FunctionTool.from_defaults(fn=execute_python)
    ssh_tool = FunctionTool.from_defaults(fn=ssh)

    tools = [
        customer_tools.faq_query_tool(),  # 该工具是QueryEngineTool--知识库检索代码
        save_file_tool, read_file_tool, list_files_tool,
        hdfs_nodes_tool,
        hdfs_exec_tool, hdfs_log_tool, hdfs_touch_tool, hdfs_disk_free_tool,
        ipinfo_tool, execute_python_tool, ssh_tool
    ]
    return tools


tools = init_tools()

agent = ReActAgent.from_tools(tools, verbose=True)

if "chat_engine" not in st.session_state.keys():
    st.session_state.chat_engine = agent

if prompt := st.chat_input("请输入你的问题："):
    chat_message = ChatMessage(role=MessageRole.USER, content=prompt)
    st.session_state.messages.append(chat_message)

for msg in st.session_state.messages:
    with st.chat_message(msg.role):
        st.write(msg.content)

if st.session_state.messages[-1].role != MessageRole.ASSISTANT:
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = st.session_state.chat_engine.stream_chat(prompt)

            text = st.write_stream(response.response_gen)

            st.session_state.messages.append(
                ChatMessage(role=MessageRole.ASSISTANT, content=text))
