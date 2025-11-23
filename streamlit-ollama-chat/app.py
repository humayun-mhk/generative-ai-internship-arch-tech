import streamlit as st
import requests

# -----------------------------------
# CONFIG
# -----------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"   # change to your installed model
# Example: "llama3.2:1b", "phi3.5", "mistral", etc.

# -----------------------------------
# STREAMLIT PAGE SETTINGS
# -----------------------------------
st.set_page_config(page_title="Local LLM Chat", layout="wide")

st.title("💬 Local LLM Chat (Ollama)")
st.subheader("Chat with an LLM running on your own machine")

# -----------------------------------
# INITIALIZE SESSION STATE
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# -----------------------------------
# FUNCTION: SEND PROMPT TO OLLAMA
# -----------------------------------
def query_ollama(prompt):
    """Send user query to Ollama Local API"""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        return f"⚠ Error: Could not reach Ollama (code {response.status_code})"


# -----------------------------------
# SIDEBAR: CONVERSATION HISTORY + RESET
# -----------------------------------
with st.sidebar:
    st.header("📝 Conversation History")

    if st.session_state["messages"]:
        for msg_type, msg in st.session_state["messages"]:
            if msg_type == "user":
                st.markdown(f"**🧑 You:** {msg}")
            else:
                st.markdown(f"**🤖 LLM:** {msg}")
    else:
        st.info("No conversation yet.")

    if st.button("🔄 Reset Conversation"):
        st.session_state["messages"] = []
        st.rerun()

# -----------------------------------
# MAIN CHAT AREA
# -----------------------------------
user_input = st.text_input("Enter your message here:")

if st.button("Send"):
    if user_input.strip() != "":
        # Save user message
        st.session_state["messages"].append(("user", user_input))

        # Query LLM
        llm_response = query_ollama(user_input)

        # Save bot response
        st.session_state["messages"].append(("bot", llm_response))

        st.rerun()

# Display chat messages below input
for msg_type, msg in st.session_state["messages"]:
    if msg_type == "user":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 LLM:** {msg}")
