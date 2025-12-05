

import streamlit as st
from openai import OpenAI
from prompt import instruction
from functions import (
    completion_func, 
    get_initial_greeting_prompt, 
    get_exit_prompt, 
    is_exit_intent, 
    build_sanitized_history,
    init_input_queue,
    add_to_queue,
    get_next_from_queue,
    has_pending_inputs,
    validate_input,
    is_processing,
    set_processing,
    efficient_completion,
    clear_queue
)
from styles import get_app_styles
import time
import json
import re
import base64
import os

def get_logo_base64():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(script_dir, "..", "logo.png")
    try:
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

logo_base64 = get_logo_base64()
logo_html_sidebar = f'<img src="data:image/png;base64,{logo_base64}" style="width: 10rem; height: 10rem; object-fit: contain;">' if logo_base64 else "🎯"
logo_html_header = f'<img src="data:image/png;base64,{logo_base64}" style="width: 7rem; height: 7rem; object-fit: contain;">' if logo_base64 else "🎯"

# Page configuration
st.set_page_config(
    page_title="TalentScout AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(get_app_styles(), unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [{"role": "system", "content": instruction}]
if "initialized" not in st.session_state:
    st.session_state.initialized = False
if "conversation_ended" not in st.session_state:
    st.session_state.conversation_ended = False
if "collected_info" not in st.session_state:
    st.session_state.collected_info = {
        "name": False,
        "contact": False,
        "location": False,
        "experience": False,
        "position": False,
        "tech_stack": False,
        "questions": False
    }

init_input_queue()

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem; display: flex; justify-content: center;">{logo_html_sidebar}</div>
        <h2 style="color: white; margin: 0;">TalentScout</h2>
        <p style="color: rgba(255,255,255,0.6); font-size: 0.9rem;">AI Hiring Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # Connection settings
    st.markdown('<div class="sidebar-card"><h3>⚙️ Connection Settings</h3></div>', unsafe_allow_html=True)
    
    base_url = st.text_input("API Base URL", value="http://localhost:11434/v1", help="Your Ollama or OpenAI-compatible API endpoint")
    model_name = st.selectbox("Model", ["llama3.1", "llama3", "mistral", "codellama"], help="Select the LLM model to use")
    
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # Interview progress
    st.markdown('<div class="sidebar-card"><h3>📋 Interview Progress</h3></div>', unsafe_allow_html=True)
    
    progress_items = [
        ("Basic Info", st.session_state.collected_info["name"]),
        ("Contact Details", st.session_state.collected_info["contact"]),
        ("Location & Exp", st.session_state.collected_info["location"]),
        ("Desired Role", st.session_state.collected_info["position"]),
        ("Tech Stack", st.session_state.collected_info["tech_stack"]),
        ("Tech Questions", st.session_state.collected_info["questions"]),
    ]
    
    for label, completed in progress_items:
        icon = "✅" if completed else "⏳"
        color = "#68d391" if completed else "rgba(255,255,255,0.5)"
        st.markdown(f'<div class="progress-item"><span style="color: {color}; font-size: 1.1rem;">{icon}</span><p style="color: white; margin: 0;">{label}</p></div>', unsafe_allow_html=True)
    
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # Quick actions
    st.markdown('<div class="sidebar-card"><h3>🚀 Quick Actions</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_history = [{"role": "system", "content": instruction}]
            st.session_state.initialized = False
            st.session_state.conversation_ended = False
            st.session_state.collected_info = {k: False for k in st.session_state.collected_info}
            st.rerun()
    
    with col2:
        if st.button("👋 End", use_container_width=True):
            if not st.session_state.conversation_ended:
                st.session_state.conversation_ended = True
                clear_queue()
                st.rerun()
    
    if st.button("🧽 Delete my data", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    
    st.markdown('<hr>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-card">
        <h3>📊 Session Stats</h3>
        <p style="font-size: 0.85rem; color: rgba(255,255,255,0.75);">
            • Your answers are used only to conduct this interview.<br>
            • We do not persist your data after the session.<br>
            • You can erase everything instantly with <b>Delete my data</b>.<br>
            • Some text is sent to the selected AI model provider, with emails/phones masked.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: center; margin-bottom: 0.5rem;">
        <span style="display: inline-flex; width: 4rem; height: 4rem;">{logo_html_header}</span>
    </div>
    <h1 style="text-align: center; margin: 0;">TalentScout AI</h1>
    <p style="text-align: center; margin-top: 0.5rem;">Your intelligent hiring assistant for tech recruitment</p>
</div>
""", unsafe_allow_html=True)

# Status indicator
if st.session_state.conversation_ended:
    st.markdown('<div class="status-badge status-ended">🔴 Interview Ended</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-badge status-active">🟢 Interview Active</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Initialize OpenAI client
@st.cache_resource
def get_client(base_url):
    return OpenAI(base_url=base_url, api_key="LAMBA")

client = get_client(base_url)

# Function to parse metadata from assistant replies
def parse_metadata_and_clean_reply(raw_reply: str):
    """
    Splits the assistant reply into:
      - display_text: what you show to the user
      - metadata: dict with booleans or None if missing
    """
    metadata = None
    display_text = raw_reply

    # Look for a line starting with METADATA:
    match = re.search(r"METADATA:\s*(\{.*\})", raw_reply, re.DOTALL)
    if match:
        json_str = match.group(1).strip()
        try:
            metadata = json.loads(json_str)
        except Exception:
            metadata = None

        # Remove the metadata part from what you show to the user
        display_text = raw_reply[:match.start()].rstrip()

    return display_text, metadata

# Initialize conversation with greeting
def initialize_conversation():
    if not st.session_state.initialized:
        with st.spinner("TalentScout is preparing..."):
            st.session_state.conversation_history.append({
                "role": "user",
                "content": get_initial_greeting_prompt()
            })
            
            try:
                completion = completion_func(client, build_sanitized_history(), model_name)
                raw_reply = completion.choices[0].message.content
                display_text, metadata = parse_metadata_and_clean_reply(raw_reply)
                
                st.session_state.conversation_history.append({"role": "assistant", "content": raw_reply})
                st.session_state.messages.append({"role": "assistant", "content": display_text})
                
                # Update progress from metadata if present
                if metadata:
                    for key in st.session_state.collected_info.keys():
                        if key in metadata and isinstance(metadata[key], bool):
                            st.session_state.collected_info[key] = metadata[key]
                
                st.session_state.initialized = True
            except Exception as e:
                st.error(f"Connection error: {str(e)}. Please check your API settings.")
                return False
    return True

# Chat display
chat_container = st.container()

with chat_container:
    # Initialize if needed
    if not st.session_state.initialized:
        initialize_conversation()
    
    # Display messages
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.markdown(f'<div class="assistant-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="user-message">{message["content"]} 👤</div>', unsafe_allow_html=True)

# Chat input
if not st.session_state.conversation_ended:
    user_input = st.chat_input("Type your message here...", key="chat_input")
    
    if user_input:
        is_valid, result = validate_input(user_input)
        
        if not is_valid:
            st.warning(result)
        else:
            add_to_queue(result)
            
            # Process all queued inputs one by one
            while has_pending_inputs():
                current_input = get_next_from_queue()
                if current_input:
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": current_input})
                    
                    # Check for exit intent
                    if is_exit_intent(current_input):
                        st.session_state.conversation_history.append({
                            "role": "user",
                            "content": get_exit_prompt()
                        })
                        st.session_state.conversation_ended = True
                        clear_queue()
                        break
                    else:
                        st.session_state.conversation_history.append({"role": "user", "content": current_input})
                    
                    # Get AI response
                    try:
                        with st.spinner("Thinking..."):
                            sanitized = build_sanitized_history()
                            raw_reply = efficient_completion(client, sanitized, model_name)
                            display_text, metadata = parse_metadata_and_clean_reply(raw_reply)
                            
                            st.session_state.conversation_history.append({"role": "assistant", "content": raw_reply})
                            st.session_state.messages.append({"role": "assistant", "content": display_text})
                            
                            if metadata:
                                for key in st.session_state.collected_info.keys():
                                    if key in metadata and isinstance(metadata[key], bool):
                                        st.session_state.collected_info[key] = metadata[key]
                                    
                    except Exception as e:
                        st.error(f"Error getting response: {str(e)}")
                        clear_queue()
                        break
            
            st.rerun()
else:
    st.info("The interview has ended. Click 'Reset' in the sidebar to start a new session.")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.4); font-size: 0.8rem; padding: 1rem;">
    Powered by TalentScout AI • Built with Streamlit
</div>
""", unsafe_allow_html=True)

