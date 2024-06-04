# The import statement will vary depending on your LLM and vector database. This is an example for OpenAI + ChromaDB
from dotenv import load_dotenv
import os
from vanna.openai.openai_chat import OpenAI_Chat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

openai_api_key = os.getenv('OPENAI_API_KEY')
model_name = os.getenv('MODEL_NAME')
openai_api_base = os.getenv('OPENAI_API_BASE')


class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)


vn = MyVanna(config={'api_key': openai_api_key, 'model': model_name, 'api_base': openai_api_base})

# See the documentation for other options
vn.ask("What are the top 10 customers by sales?")