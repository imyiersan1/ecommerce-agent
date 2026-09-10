from app.graph import graph

if __name__ == "__main__":
    print("🤖 电商客服 Agent 已启动！(输入 'quit' 退出)")
    
    # thread_id 相当于一个会话 ID，同一个 ID 共享记忆
    config = {"configurable": {"thread_id": "user_001"}}
    
    while True:
        user_input = input("\n你: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("客服: 再见！期待下次为您服务！")
            break
            
        # 调用图，传入用户输入
        result = graph.invoke(
            {"user_input": user_input, "intent": "", "answer": ""},
            config=config
        )
        
        print(f"客服: {result['answer']}")