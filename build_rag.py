import os
import shutil
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 0. 自动清理旧的向量数据库，防止重复叠加
if os.path.exists("./chroma_db"):
    print("检测到旧的向量数据库，正在清理...")
    shutil.rmtree("./chroma_db")

print("1. 正在加载商品手册...")
loader = TextLoader("product_manual.txt", encoding="utf-8")
documents = loader.load()

print("2. 正在进行智能文档切片...")
# 使用递归分割器，按段落 -> 换行 -> 句号 逐级切分，保留上下文
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,       # 每片大约200字
    chunk_overlap=30,     # 相邻切片重叠30字，防止上下文断裂
    separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""]
)
docs = text_splitter.split_documents(documents)
print(f"共切分出 {len(docs)} 个文档片段。")

print("3. 正在加载本地向量模型...")
# 注意：第一次运行会下载约100MB的模型，请耐心等待
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")

print("4. 正在存入向量数据库 Chroma...")
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
print("✅ RAG 向量数据库构建成功！")