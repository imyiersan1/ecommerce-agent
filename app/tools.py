import os
import sqlite3

# 强制使用国内镜像（必须放在加载向量模型之前）
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from langchain_core.tools import tool
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 全局初始化一次向量模型和数据库
print("正在加载本地向量模型和 Chroma 数据库...")
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs={'local_files_only': True}
)
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# 1. 定义订单查询工具
@tool
def query_order_db(order_id: str) -> str:
    """
    根据订单号查询订单状态和物流信息。
    :param order_id: 订单号字符串
    :return: 查询结果
    """
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status, logistics FROM orders WHERE order_id = ?", (order_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return f"订单状态：{result[0]}，物流信息：{result[1]}"
    else:
        return "未找到该订单号，请核对后重试。"

# 2. 定义 RAG 知识库检索工具
@tool
def rag_query_product(query: str) -> str:
    """
    根据用户的商品咨询问题，去商品知识库中进行检索。
    适用于查询商品参数、活动优惠、售后退换货规则等非结构化问题。
    :param query: 用户的提问或商品关键词
    :return: 检索到的相关文档片段
    """
    docs = vectorstore.similarity_search(query, k=2)
    if not docs:
        return "知识库中未找到相关商品信息。"
    
    results = "\n\n".join([doc.page_content for doc in docs])
    return f"从知识库检索到以下内容：\n{results}"

# 3. 把所有工具放进列表（工单工具将通过 MCP 动态加载，不写在这里）
tools = [query_order_db, rag_query_product]