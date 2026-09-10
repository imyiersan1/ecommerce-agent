# app/mcp_client.py
from langchain_mcp_adapters.client import MultiServerMCPClient

async def load_mcp_tools():
    """连接 MCP Server，加载其提供的所有工具"""
    client = MultiServerMCPClient({
        "ticket": {
            "command": "python",
            "args": ["mcp_server.py"],  # 指向你的 mcp_server.py 文件
            "transport": "stdio",
        }
    })
    tools = await client.get_tools()
    return tools