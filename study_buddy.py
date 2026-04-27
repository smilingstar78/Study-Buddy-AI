import streamlit as st
import time
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ----------------------------
# 🔑 API KEY (Streamlit Secrets)
# ----------------------------
api_key = st.secrets["GOOGLE_API_KEY"]

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=api_key
)

# ----------------------------
# 🎀 PAGE CONFIG (LOCK LIGHT MODE FEEL)
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
<p style="text-align:center; color:#666;">
your cute AI tutor 📚💖
</p>
""", unsafe_allow_html=True)

# ----------------------------
# 🎨 FIXED KAWAII UI (NO DARK MODE BREAK)
# ----------------------------
st.markdown("""
<style>

/* FORCE LIGHT STABLE BACKGROUND */
html, body, .stApp {
    background-color: #fff7fb !important;
    color: #222 !important;
}

/* CHAT WRAPPER */
.chat-box {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 90px;
}

/* ROW */
.row {
    display: flex;
    width: 100%;
}

/* USER RIGHT */
.user-row {
    justify-content: flex-end;
}

/* AI LEFT */
.ai-row {
    justify-content: flex-start;
}

/* CHAT BUBBLE (IMPORTANT: FIT CONTENT) */
.bubble {
    padding: 10px 14px;
    border-radius: 16px;
    width: fit-content;
    max-width: 70%;
    word-wrap: break-word;
    font-size: 15px;
    line-height: 1.4;
    margin: 4px 0;
}

/* USER STYLE */
.user {
    background-color: #ffd6e7;
    color: #222;
}

/* AI STYLE */
.ai {
    background-color: #dff6ff;
    color: #222;
}

/* INPUT STYLE FIX */
.stChatInputContainer {
    background: white !important;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# 🧠 SYSTEM PROMPT
# ----------------------------
system_prompt = SystemMessage(content="""
You are Study Buddy AI 🌸

Rules:
- Explain simply
- Give examples
- Stay focused on learning
- Be friendly and supportive
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

# show chat
render_chat()

# ----------------------------
# ✍️ INPUT
# ----------------------------
user_input = st.chat_input("Ask me anything 📚✨")

# ----------------------------
# 🚀 USER MESSAGE HANDLING
# ----------------------------
if user_input:

    # instantly show user message
    st.session_state.chat_history.append(
        HumanMessage(content=user_input)
    )

    st.rerun()

# ----------------------------
# 🤖 AI RESPONSE FLOW
# ----------------------------
if len(st.session_state.chat_history) > 0:
    last_msg = st.session_state.chat_history[-1]

    if isinstance(last_msg, HumanMessage):

        # smooth thinking effect
        with st.spinner("🤖 AI is thinking... ●●●"):
            time.sleep(0.7)
            response = model.invoke(st.session_state.chat_history)

        st.session_state.chat_history.append(
            AIMessage(content=response.content)
        )

        st.rerun()