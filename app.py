"""
AI Agent Dashboard - Streamlit Application
A simple interactive dashboard for interacting with an AI agent.
"""

import streamlit as st
from agent import create_agent

# Page configuration
st.set_page_config(
    page_title="AI Agent Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
        .main-title {
            color: #1f77b4;
            font-size: 2.5em;
            margin-bottom: 0.5em;
        }
        .success-box {
            padding: 1em;
            border-radius: 0.5em;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .info-box {
            padding: 1em;
            border-radius: 0.5em;
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = None
    st.session_state.conversation_history = []
    st.session_state.initialization_error = None

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.divider()
    
    # Agent initialization
    st.subheader("Agent Settings")
    
    model_option = st.selectbox(
        "Select Model",
        options=["deepseek-chat"],
        help="Choose the AI model to use"
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative, Lower = more deterministic"
    )
    
    if st.button("🔄 Initialize Agent", key="init_button", use_container_width=True):
        try:
            st.session_state.agent = create_agent(
                model=model_option,
                temperature=temperature
            )
            st.session_state.initialization_error = None
            st.success("✓ Agent initialized successfully!")
        except ValueError as e:
            st.session_state.initialization_error = str(e)
            st.error(f"❌ Initialization failed: {str(e)}")
    
    st.divider()
    
    # Conversation management
    st.subheader("Conversation")
    
    if st.button("🗑️ Clear History", use_container_width=True):
        if st.session_state.agent:
            st.session_state.agent.reset_conversation()
            st.session_state.conversation_history = []
            st.success("History cleared!")
        else:
            st.warning("No agent initialized")
    
    st.divider()
    
    # Info section
    st.subheader("ℹ️ About")
    st.markdown("""
    **AI Agent Dashboard**
    
    A simple interface for interacting with an LLM-based AI agent.
    
    - Initialize the agent first
    - Enter your query in the main area
    - View responses and conversation history
    """)

# Main Content Area
st.markdown('<h1 class="main-title">AI Agent Dashboard</h1>', unsafe_allow_html=True)
st.markdown("Ask questions and get intelligent responses from the AI agent.")

# Check if agent is initialized
if st.session_state.agent is None:
    st.info(
        "👈 **Configure the agent in the sidebar** and click 'Initialize Agent' to get started.",
        icon="ℹ️"
    )
    if st.session_state.initialization_error:
        st.error(f"**Error:** {st.session_state.initialization_error}")
else:
    st.success("✓ Agent is ready", icon="✅")

st.divider()

# Input and interaction
col1, col2 = st.columns([4, 1])

with col1:
    user_input = st.text_area(
        "Enter your question or prompt:",
        height=100,
        placeholder="Ask me anything...",
        label_visibility="collapsed"
    )

with col2:
    submit_button = st.button("📤 Submit", use_container_width=True)

# Process user input
if submit_button:
    if st.session_state.agent is None:
        st.error("❌ Please initialize the agent first using the sidebar configuration.")
    elif not user_input.strip():
        st.warning("⚠️ Please enter a question or prompt.")
    else:
        # Show processing indicator
        with st.spinner("🤔 Agent is processing..."):
            try:
                # Get response from agent
                response = st.session_state.agent.process(user_input)
                
                # Store in history
                st.session_state.conversation_history.append({
                    "type": "user",
                    "content": user_input
                })
                st.session_state.conversation_history.append({
                    "type": "assistant",
                    "content": response
                })
                
                # Display success message
                st.success("✓ Response received!")
                
                # Display the response
                st.markdown("### Agent Response:")
                st.markdown(f'<div class="info-box">{response}</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Conversation History Section
if st.session_state.conversation_history:
    st.divider()
    st.subheader("💬 Conversation History")
    
    # Display conversation in chronological order
    for msg in st.session_state.conversation_history:
        if msg["type"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:  # assistant
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

# Footer
st.divider()
st.markdown(
    """
    <hr>
    <p style="text-align: center; color: gray; font-size: 0.9em;">
        AI Agent Dashboard | Mini-Assignment 5 | IIMT3688
    </p>
    """,
    unsafe_allow_html=True
)
