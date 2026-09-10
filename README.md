# 🤖 电商客服智能体 (E-commerce Customer Service Agent)

基于 **LangGraph + DeepSeek + RAG** 打造的一站式电商智能客服系统。具备自主任务规划、工具动态调度、知识库检索以及多轮对话记忆能力，通过 FastAPI 封装后端接口，并配备 Streamlit 前端界面进行交互展示。

## ✨ 核心功能

- **智能意图识别与路由**：使用大模型精准识别用户意图（订单查询/商品咨询/售后退款），基于 LangGraph 的条件边动态分发到对应处理节点。
- **多工具自主调度 (Tool Calling)**：大模型自主判断是否需要调用工具。支持调用 SQLite 订单数据库查询物流状态，以及调用 RAG 知识库查询商品信息。
- **RAG 检索增强生成**：内置完整 RAG 链路。基于 Chroma 向量数据库 + BAAI/bge-small-zh-v1.5 中文向量模型，实现对商品文档切片、向量化存储及相似性检索。
- **多轮对话记忆**：基于 LangGraph 的 `MemorySaver` 和动态 `thread_id`，实现上下文记忆，支持“开启新对话”进行会话隔离。
- **服务化封装**：使用 FastAPI 将 LangGraph 智能体封装为标准的 HTTP RESTful 接口（`/chat`），方便与外部业务系统对接。
- **可视化交互界面**：使用 Streamlit 构建极简现代化的聊天界面，包含欢迎引导卡片、会话状态显示及一键开启新对话功能。

## 🏗️ 系统架构图

```mermaid
graph TD
    User[用户输入] --> Intent[意图识别节点]
    Intent --> Route{条件路由}
    
    Route -->|order| OrderNode[订单处理节点]
    Route -->|product| ProductNode[商品处理节点]
    Route -->|refund| RefundNode[退款处理节点]
    Route -->|unknown| UnknownNode[兜底回复节点]
    
    OrderNode -->|大模型自主决策| Tool1[query_order_db 工具]
    ProductNode -->|大模型自主决策| Tool2[rag_query_product 工具]
    
    Tool1 --> SQLite[(SQLite 订单数据库)]
    Tool2 --> VectorDB[(Chroma 向量数据库)]
    
    SQLite --> Result[返回查询结果]
    VectorDB --> Result
    RefundNode --> Result
    UnknownNode --> Result
    Result --> End[结束]
