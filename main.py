from llama_index.core import Settings
from llama_index.core.chat_engine import SimpleChatEngine

from llms.LLMs import deepseek_llm

llm = deepseek_llm(temperature=0.7,
                   system_prompt="你是一位人工智能助手，可以帮助用户解决各种问题，请确保你的回答准确且简洁。")
# 下面代码基本都不需要再传入大模型参数
Settings.llm = llm
chat_engine = SimpleChatEngine.from_defaults()
response = chat_engine.stream_chat("你好")
print(response)

