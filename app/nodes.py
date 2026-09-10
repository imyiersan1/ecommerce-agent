from .config import llm, llm_with_tools
from .state import AgentState
from .tools import query_order_db, rag_query_product
from langchain_core.messages import ToolMessage

# 1. 意图识别节点
def classify_intent(state: AgentState):
    text = state["user_input"]
    prompt = f"""你是一个电商客服意图识别助手。
请判断用户的意图属于以下哪一类：
- order (订单物流查询)
- refund (售后退款)
- product (商品咨询)
- unknown (其他)

只输出一个英文单词，不要输出任何其他内容。
用户输入：{text}
"""
    response = llm.invoke(prompt)
    intent = response.content.strip().lower()
    
    if "order" in intent: intent = "order"
    elif "refund" in intent: intent = "refund"
    elif "product" in intent: intent = "product"
    else: intent = "unknown"
    
    print(f"\n【大模型识别结果】: {intent}")
    return {"intent": intent}

# 2. 路由函数（根据意图分发到不同节点）
def route_by_intent(state: AgentState):
    intent = state["intent"]
    if intent == "order": return "handle_order"
    elif intent == "refund": return "handle_refund"
    elif intent == "product": return "handle_product"
    else: return "handle_unknown"

# 3. 订单处理节点（大模型自主决定是否调用订单数据库工具）
def handle_order(state: AgentState):
    print("【节点执行】: 进入订单处理节点，交由大模型自主决策...")
    
    messages = [
        ("system", "你是一个电商客服。如果用户要查询订单，请调用 query_order_db 工具。如果用户没有提供订单号，请直接回复请求他提供订单号，不要调用工具。"),
        ("user", state["user_input"])
    ]
    
    response = llm_with_tools.invoke(messages)
    
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        print(f"【大模型决策】: 发现需要调用工具 {tool_call['name']}，参数: {tool_call['args']}")
        
        tool_result = query_order_db.invoke(tool_call['args'])
        print(f"【工具执行结果】: {tool_result}")
        
        return {"answer": tool_result, "messages": [response, ToolMessage(content=tool_result, tool_call_id=tool_call['id'])]}
    else:
        print("【大模型决策】: 不需要调用工具，直接回复。")
        return {"answer": response.content, "messages": [response]}

# 4. 商品处理节点（大模型自主决定是否调用 RAG 向量检索工具）
def handle_product(state: AgentState):
    print("【节点执行】: 进入商品处理节点，交由大模型自主决策（RAG检索）...")
    
    messages = [
        # 注意：这里的 System Prompt 已经优化，不再纠结型号，直接去检索
        ("system", "你是一个电商客服。如果用户要查询商品信息、优惠活动、售后规则或清洗保养方法，请立即调用 rag_query_product 工具，把用户的完整问题作为检索词。只有当用户完全没有提到任何商品名称（例如只说‘怎么洗’、‘有什么优惠’）时，才回复请求补充信息。不要纠结于具体的型号，直接用通用关键词去检索。"),
        ("user", state["user_input"])
    ]
    
    response = llm_with_tools.invoke(messages)
    
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        print(f"【大模型决策】: 发现需要调用工具 {tool_call['name']}，参数: {tool_call['args']}")
        
        tool_result = rag_query_product.invoke(tool_call['args'])
        print(f"【工具执行结果】: {tool_result}")
        
        return {"answer": tool_result, "messages": [response, ToolMessage(content=tool_result, tool_call_id=tool_call['id'])]}
    else:
        print("【大模型决策】: 不需要调用工具，直接回复。")
        return {"answer": response.content, "messages": [response]}

# 5. 退款处理节点（暂用模拟回复占位）
def handle_refund(state: AgentState):
    print("【节点执行】: 正在进入退款/工单节点...")
    return {"answer": "已进入售后系统，正在为你生成退款工单..."}

# 6. 兜底回复节点
def handle_unknown(state: AgentState):
    print("【节点执行】: 进入兜底回复节点...")
    return {"answer": "抱歉，我没太理解您的诉求，能详细描述一下吗？"}