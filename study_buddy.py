import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ----------------------------
# 🔑 API KEY
# ----------------------------
api_key = st.secrets["GOOGLE_API_KEY"]

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=api_key
)

# ----------------------------
# 🎀 PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Study Buddy AI",
    page_icon="🌸",
    layout="centered"
)

# ----------------------------
# 🌸 HEADER
# ----------------------------
st.markdown("""
<h1 style="text-align:center; color:#ff4d88;">🌸 Study Buddy AI ✨</h1>
<p style="text-align:center; color:#666;">your cute AI tutor 📚💖</p>
""", unsafe_allow_html=True)

# ----------------------------
# 🎨 UI
# ----------------------------
st.markdown("""
<style>
html, body, .stApp {
    background-color: #fff7fb !important;
    color: #222 !important;
}

.user-row {
    display: flex;
    justify-content: flex-end;
}

.ai-row {
    display: flex;
    justify-content: flex-start;
}

.bubble {
    padding: 10px 14px;
    border-radius: 16px;
    width: fit-content;
    max-width: 75%;
    word-wrap: break-word;
    margin: 6px 0;
}

.user { background: #ffd6e7; }
.ai { background: #dff6ff; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 🧠 SYSTEM PROMPT
# ----------------------------
system_prompt = SystemMessage(content="""
You are Study Buddy AI 🌸
Explain simply and help users learn.
""")

# ----------------------------
# 💬 SESSION
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [system_prompt]

# ----------------------------
# 💬 DISPLAY CHAT
# ----------------------------
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.markdown(f"<div class='user-row'><div class='bubble user'>{msg.content}</div></div>", unsafe_allow_html=True)
    elif isinstance(msg, AIMessage):
        st.markdown(f"<div class='ai-row'><div class='bubble ai'>{msg.content}</div></div>", unsafe_allow_html=True)

# ----------------------------
# ✍️ INPUT
# ----------------------------
user_input = st.chat_input("Ask something...")

if user_input:
    # show user instantly
    st.session_state.messages.append(HumanMessage(content=user_input))

    # show typing
    with st.spinner("🤖 Thinking..."):
        response = model.invoke(st.session_state.messages)

    # show AI response
    st.session_state.messages.append(AIMessage(content=response.content))

    st.rerun()
