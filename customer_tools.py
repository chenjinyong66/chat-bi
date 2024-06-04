import openai
from llama_index.core import StorageContext, load_index_from_storage, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata

openai.api_key = "sk-JxLAjLyiAoUAfgFE901c6b823bC84e8bA81042CbA0Bd8188"
openai.base_url = "https://api.xty.app/v1"


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
