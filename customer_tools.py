import socket
from typing import Dict

import paramiko
from llama_index.core import StorageContext, load_index_from_storage, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata


def faq_query_tool():
    index = None
    try:
        storage_context = StorageContext.from_defaults(
            persist_dir="./storage/faq"
        )
        index = load_index_from_storage(storage_context)

        index_loaded = True
    except:
        index_loaded = False
    if not index_loaded:
        # load data
        docs = SimpleDirectoryReader(
            input_files=["./ecommerce_data/faq.txt"]
        ).load_data()
        # build index
        index = VectorStoreIndex.from_documents(docs)

        # persist index
        index.storage_context.persist(persist_dir="./storage/faq")

    query_engine_tool = QueryEngineTool(
        query_engine=index.as_query_engine(similarity_top_k=3),
        metadata=ToolMetadata(
            name="faq_data",
            description=(
                "Provides information and answers to FAQ about e-commerce systems. "
                "Use a detailed plain text question as input to the tool."
            ),
            # return_direct=True,
        ),
    )
    return query_engine_tool


def recommend_product(query=None):
    """
    useful for when you need to answer questions about product recommendations
    :param query:
    :return:
    """
    return "红色连衣裙"


def search_order(query=None):
    """
     一个帮助用户查询最新订单状态的工具，并且能处理以下情况:
    1.在用户没有输入订单号的时候，会询问用户订单号
    2.在用户输入的订单号查询不到的时候，会让用户二次确认订单号是否正确
    :param query:
    :return:
    """
    return {
        "id": 2,
        "order_number": "20240101XYZ",
        "status": "处理中",
        "shipping_date": "2024-05-31",
        "estimated_delivered_date": "2024-06-09"
    }


def get_namenodes(query=None):
    """
       查询hdfs namenode节点信息
       Get the namenode list of the HDFS cluster.
       :param query:
       :return:
       """

    res = exec_command_on_hdfs(command="cd /opt/datasophon/hadoop-3.3.3/logs && tail -n 30 hadoop-hdfs-namenode-*.log")

    return res['stdout'][-2000:]


def exec_command_on_hdfs(host: str = "10.212.1.67", username: str = "root", password: str = "KGwydata!@#",
                         command: str = "",
                         timeout: int = 5) -> Dict:
    """
    建立SSH连接到HDFS主机，执行命令，并返回命令输出。

    参数:
    - host: HDFS主机的IP地址或主机名。
    - username: SSH登录用户名，默认为"root"。
    - password: SSH登录密码，默认为"KGwydata!@#"。
    - command: 要在HDFS上执行的命令。
    - timeout: 命令执行的超时时间，默认为5秒。

    返回:
    - 包含命令输出和错误信息的字典。
    """
    # 初始化SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # 建立SSH连接
        client.connect(host, username=username, password=password)

        # 执行命令
        stdin, stdout, stderr = client.exec_command(command)
        stdout.channel.settimeout(timeout)
        retcode = 999

        try:
            output_stdout = stdout.read().decode('utf-8')
            output_stderr = stderr.read().decode('utf-8')
            retcode = stdout.channel.recv_exit_status()
        except socket.timeout:
            output_stdout = ""
            output_stderr = ""
            while True:
                try:
                    output_stdout += stdout.readline().decode('utf-8') + "\n"
                except socket.timeout:
                    break
            while True:
                try:
                    output_stderr += stderr.readline().decode('utf-8') + "\n"
                except socket.timeout:
                    break

        return {
            "stdout": output_stdout,
            "stderr": output_stderr,
            "exitStatus": retcode
        }
    finally:
        # 关闭连接
        client.close()
