import streamlit as st
import uuid
from app.graph import graph

# ================= 页面配置 =================
st.set_page_config(page_title="电商客服 Agent", page_icon="🤖", layout="centered")

# ================= 注入 CSS（打造现代化界面） =================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 聊天背景 */
    .stApp { background-color: #f7f9fc; }
    
    /* 聊天气泡样式 */
    [data-testid="stChatMessage"] {
        background-color: white; 
        border-radius: 12px;
        padding: 15px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 12px;
    }
    
    /* 输入框样式 */
    .stChatInput { border-radius: 24px; border: 1px solid #e0e0e0; }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ================= 初始化 Session State =================
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# ================= 侧边栏（控制台） =================
with st.sidebar:
    st.title("⚙️ 控制台")
    
    # 开启新对话按钮
    if st.button("➕ 开启新对话", use_container_width=True, type="primary"):
        st.session_state.thread_id = str(uuid.uuid4()) # 生成全新会话ID
        st.session_state.messages = []                # 清空前端历史
        st.rerun()                                    # 刷新页面
        
    st.markdown("---")
    
    # 当前会话信息
    st.subheader("💬 当前会话")
    st.caption(f"ID: `{st.session_state.thread_id[:8]}...`")
    st.caption("状态：已记忆上下文")
    
    st.markdown("---")
    st.caption("🤖 智能客服演示系统")

# ================= 主界面 =================
st.title("🤖 电商客服智能体")
st.caption("支持订单查询 / 商品咨询 / 售后工单")

# 如果没有历史消息，显示欢迎卡片和引导问题
if len(st.session_state.messages) == 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👋 您好！我是您的专属电商客服，请问有什么可以帮您？")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📦 查订单物流 (比如：查一下订单 123456 的物流)", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "查一下订单 123456 的物流"})
            st.rerun()
    with col2:
        if st.button("🛍️ 问商品参数 (比如：帆布包怎么洗？)", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "帆布包怎么洗？"})
            st.rerun()

# 渲染历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# 接收用户输入并调用 Agent
if prompt := st.chat_input("请输入您的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("客服正在思考中..."):
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            result = graph.invoke(
                {"user_input": prompt, "intent": "", "answer": ""},
                config=config
            )
            answer = result["answer"]
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})