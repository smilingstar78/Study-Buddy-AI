import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ----------------------------
# 🔑 API KEY
# ----------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("🚨 API key not found. Add it in Streamlit Secrets.")
    st.stop()

# ----------------------------
# 🤖 MODEL
# ----------------------------
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",   # stable + fast
    api_key=api_key,
    temperature=0.7
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
<p style="text-align:center; color:#666;">
fast + cute AI tutor 📚💖
</p>
""", unsafe_allow_html=True)

# ----------------------------
# 🎨 UI (FORCE LIGHT MODE)
# ----------------------------
st.markdown("""
<style>

html, body, .stApp {
    background-color: #fff7fb !important;
    color: #222 !important;
}

/* USER RIGHT */
.user-row {
    display: flex;
    justify-content: flex-end;
}

/* AI LEFT */
.ai-row {
    display: flex;
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
    margin: 6px 0;
}

/* USER */
.user {
    background-color: #ffd6e7;
}

/* AI */
.ai {
    background-color: #dff6ff;
}

/* INPUT */
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
            <div class="user-row">
                <div class="bubble user">🧑‍🎓 {msg.content}</div>
            </div>
            """, unsafe_allow_html=True)

        elif isinstance(msg, AIMessage):
            st.markdown(f"""
            <div class="ai-row">
                <div class="bubble ai">🤖 {msg.content}</div>
            </div>
            """, unsafe_allow_html=True)

render_chat()

# ----------------------------
# 🧪 TEST BUTTON (DEBUG)
# ----------------------------
if st.button("🔍 Test API"):
    try:
        res = model.invoke([HumanMessage(content="Hello")])
        st.success("✅ API Working!")
        st.write(res.content)
    except Exception as e:
        st.error(f"❌ API Error: {e}")

# ----------------------------
# ✍️ INPUT
# ----------------------------
user_input = st.chat_input("Ask me anything 📚✨")

# ----------------------------
# 🚀 USER MESSAGE
# ----------------------------
if user_input and user_input.strip():

    st.session_state.chat_history.append(
        HumanMessage(content=user_input)
    )

    st.rerun()

# ----------------------------
# 🤖 AI RESPONSE (SAFE)
# ----------------------------
if len(st.session_state.chat_history) > 0:

    last_msg = st.session_state.chat_history[-1]

    if isinstance(last_msg, HumanMessage):

        placeholder = st.empty()
        placeholder.markdown("🤖 AI is typing...")

        try:
            # reduce tokens (important for speed + avoid errors)
            st.session_state.chat_history = (
                [system_prompt] + st.session_state.chat_history[-4:]
            )

            response = model.invoke(st.session_state.chat_history)

            placeholder.empty()

            st.session_state.chat_history.append(
                AIMessage(content=response.content)
            )

        except Exception as e:
            placeholder.empty()
            st.error(f"⚠️ ERROR: {e}")
            print("FULL ERROR:", e)

        st.rerun()
