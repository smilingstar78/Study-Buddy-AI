import streamlit as st
import time
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ----------------------------
# 🔑 API KEY
# ----------------------------
load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY")
)

# ----------------------------
# 🎀 PAGE SETUP
# ----------------------------
st.set_page_config(
    page_title="Study Buddy AI",
    page_icon="🌸",
    layout="centered"
)

st.markdown("""
<h1 style='text-align:center; color:#ff4d88;'>🌸 Study Buddy AI ✨</h1>
<p style='text-align:center; color:#666;'>your cute AI study buddy 📚💖</p>
""", unsafe_allow_html=True)

# ----------------------------
# 🎨 KAWAII CHAT CSS
# ----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #fff5f8, #e6f7ff);
}

/* CHAT CONTAINER */
.chat-box {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 80px;
}

/* ROW WRAPPER */
.row {
    display: flex;
    width: 100%;
}

/* USER RIGHT SIDE */
.user-row {
    justify-content: flex-end;
}

/* AI LEFT SIDE */
.ai-row {
    justify-content: flex-start;
}

/* COMMON BUBBLE */
.bubble {
    padding: 10px 14px;
    border-radius: 16px;
    max-width: 70%;
    width: fit-content;
    word-wrap: break-word;
    font-size: 15px;
}

/* USER STYLE */
.user {
    background-color: #ffe4ec;
    text-align: left;
}

/* AI STYLE */
.ai {
    background-color: #e6f7ff;
    text-align: left;
}

/* TYPOGRAPHY */
p {
    margin: 0;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# 🧠 SYSTEM PROMPT
# ----------------------------
system_prompt = SystemMessage(content="""
You are Study Buddy AI 🌸
- Explain simply
- Use examples
- Stay focused on learning
""")

# ----------------------------
# 💬 SESSION STATE
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [system_prompt]

# ----------------------------
# 💬 RENDER CHAT
# ----------------------------
def render_chat():
    for msg in st.session_state.chat_history:

        if isinstance(msg, HumanMessage):
            st.markdown(f"""
            <div class="row user-row">
                <div class="bubble user">🧑‍🎓 {msg.content}</div>
            </div>
            """, unsafe_allow_html=True)

        elif isinstance(msg, AIMessage):
            st.markdown(f"""
            <div class="row ai-row">
                <div class="bubble ai">🤖 {msg.content}</div>
            </div>
            """, unsafe_allow_html=True)

# ----------------------------
# SHOW CHAT
# ----------------------------
render_chat()

# ----------------------------
# INPUT
# ----------------------------
user_input = st.chat_input("Ask me anything 📚✨")

# ----------------------------
# LOGIC
# ----------------------------
if user_input:

    # add user message
    st.session_state.chat_history.append(
        HumanMessage(content=user_input)
    )

    st.rerun()

# AFTER rerun → generate AI response
if len(st.session_state.chat_history) > 0:
    last_msg = st.session_state.chat_history[-1]

    if isinstance(last_msg, HumanMessage):

        with st.spinner("🤖 AI is thinking..."):
            time.sleep(0.7)
            response = model.invoke(st.session_state.chat_history)

        st.session_state.chat_history.append(
            AIMessage(content=response.content)
        )

        st.rerun()