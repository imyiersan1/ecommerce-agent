import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from .tools import tools

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    temperature=0.0
)

# 将最新的工具列表绑定给大模型
llm_with_tools = llm.bind_tools(tools)