import streamlit as st
import time

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ----------------------------
# 🔑 API KEY (STREAMLIT SECRETS)
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
<h1 style='text-align:center; color:#ff4d88;'>🌸 Study Buddy AI ✨</h1>
<p style='text-align:center; color:#666; text-align:center;'>
your cute AI tutor for learning 📚💖
</p>
""", unsafe_allow_html=True)

# ----------------------------
# 🎨 KAWAII CHAT UI CSS
# ----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #fff5f8, #e6f7ff);
}

/* CHAT WRAPPER */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 80px;
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

/* BUBBLE */
.bubble {
    padding: 10px 14px;
    border-radius: 16px;
    width: fit-content;
    max-width: 75%;
    word-wrap: break-word;
    font-size: 15px;
}

/* USER STYLE */
.user {
    background-color: #ffe4ec;
    color: #222;
}

/* AI STYLE */
.ai {
    background-color: #e6f7ff;
    color: #222;
}

/* small animation feel */
.bubble {
    animation: fadeIn 0.2s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# 🧠 SYSTEM PROMPT
# ----------------------------
system_prompt = SystemMessage(content="""
You are Study Buddy AI 🌸

Rules:
- Explain concepts simply
- Use examples when needed
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
user_input = st.chat_input("Ask me anything to learn 📚✨")

# ----------------------------
# 🚀 LOGIC
# ----------------------------
if user_input:

    # 1. show user instantly
    st.session_state.chat_history.append(
        HumanMessage(content=user_input)
    )

    st.rerun()

# ----------------------------
# 🤖 AI RESPONSE (after rerun)
# ----------------------------
if len(st.session_state.chat_history) > 0:
    last_msg = st.session_state.chat_history[-1]

    if isinstance(last_msg, HumanMessage):

        # typing effect
        with st.spinner("🤖 AI is thinking... ●●●"):
            time.sleep(0.7)

            response = model.invoke(st.session_state.chat_history)

        st.session_state.chat_history.append(
            AIMessage(content=response.content)
        )

        st.rerun()