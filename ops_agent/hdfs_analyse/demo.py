#!/usr/bin/python
# -*- coding: UTF-8 -*-
from dotenv import load_dotenv
import os
import sys

sys.path.insert(0, os.path.split(os.path.realpath(__file__))[0] + "/../")

from ops_agent.aibond import AI

from hdfscluster import HDFSCluster

from langchain_openai import ChatOpenAI

model = ChatOpenAI(openai_api_key="sk-149bf3c0b0e543609274d93ffec44824", openai_api_base="https://api.deepseek.com/v1",
                   model_name="deepseek-chat")

load_dotenv()

ai = AI()
openai_api_key = os.getenv('OPENAI_API_KEY')
model_name = os.getenv('MODEL_NAME')
openai_api_base = os.getenv('OPENAI_API_BASE')

resp = ai.run("当前这个集群[10.212.1.67]正常吗？",
              llm=model,
              tools=[HDFSCluster("10.212.1.67")], verbose=True)
print("=== resp ===")
print(resp)
