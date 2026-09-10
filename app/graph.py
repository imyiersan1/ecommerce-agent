from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from .state import AgentState
from .nodes import (
    classify_intent, route_by_intent,
    handle_order, handle_refund, handle_product, handle_unknown
)

def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("classify_intent", classify_intent)
    builder.add_node("handle_order", handle_order)
    builder.add_node("handle_refund", handle_refund)
    builder.add_node("handle_product", handle_product)
    builder.add_node("handle_unknown", handle_unknown)

    builder.add_edge(START, "classify_intent")

    builder.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "handle_order": "handle_order",
            "handle_refund": "handle_refund",
            "handle_product": "handle_product",
            "handle_unknown": "handle_unknown"
        }
    )

    builder.add_edge("handle_order", END)
    builder.add_edge("handle_refund", END)
    builder.add_edge("handle_product", END)
    builder.add_edge("handle_unknown", END)

    # 核心：加入记忆存储
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)

graph = build_graph()