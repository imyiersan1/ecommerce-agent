from fastapi import FastAPI
from pydantic import BaseModel
from .graph import graph

# 创建 FastAPI 应用
app = FastAPI(title="电商客服 Agent API")

# 定义请求体格式
class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_user" # 会话ID，用于区分不同用户的记忆

# 定义响应体格式
class ChatResponse(BaseModel):
    answer: str

# 核心接口：对话聊天
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 配置会话记忆ID
    config = {"configurable": {"thread_id": request.thread_id}}
    
    # 调用 LangGraph 图
    result = graph.invoke(
        {"user_input": request.message, "intent": "", "answer": ""},
        config=config
    )
    
    return ChatResponse(answer=result["answer"])

# 健康检查接口
@app.get("/health")
async def health():
    return {"status": "ok"}