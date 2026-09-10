# mcp_server.py
from mcp.server.fastmcp import FastMCP

# 创建 MCP Server
mcp = FastMCP("Ecommerce Ticket Server")

# 内存中的工单数据库（模拟）
tickets = []

@mcp.tool()
def create_refund_ticket(order_id: str, reason: str) -> str:
    """
    为指定订单创建退换货工单。
    :param order_id: 订单号
    :param reason: 退换货原因
    :return: 工单创建结果
    """
    ticket_id = f"TK{len(tickets) + 1:04d}"
    tickets.append({"ticket_id": ticket_id, "order_id": order_id, "reason": reason, "status": "已创建"})
    return f"工单已创建成功，工单号：{ticket_id}，关联订单：{order_id}，原因：{reason}"

@mcp.tool()
def query_ticket_status(ticket_id: str) -> str:
    """
    根据工单号查询工单状态。
    :param ticket_id: 工单号
    :return: 工单状态信息
    """
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            return f"工单 {ticket_id} 状态：{t['status']}，关联订单：{t['order_id']}"
    return f"未找到工单号 {ticket_id}"

if __name__ == "__main__":
    mcp.run(transport="stdio")