# app.py

import re
import streamlit as st
from simple_salesforce import Salesforce
from autogen import AssistantAgent, ConversableAgent, GroupChat, GroupChatManager
from autogen.coding import LocalCommandLineCodeExecutor

# Load credentials from Streamlit secrets
sf_creds = st.secrets["salesforce"]
azure_config = st.secrets["azure"]

# Initialize Salesforce connection
sf = Salesforce(
    username=sf_creds["username"],
    password=sf_creds["password"],
    security_token=sf_creds["security_token"],
    domain=sf_creds["domain"]
)

# Initialize Assistant Agent
assistant = AssistantAgent(
    name="assistant",
    system_message="""You are a Salesforce CPQ expert. Generate Python code using simple_salesforce library.
    Ensure the code is executable and handles Salesforce API responses properly.""",
    llm_config={
        "config_list": [{
            "model": "productgpt-4",
            "api_type": "azure",
            "api_key": azure_config["api_key"],
            "base_url": azure_config["base_url"],
            "api_version": azure_config["api_version"]
        }]
    },
    human_input_mode="NEVER"
)

# Initialize Code Executor
code_executor = LocalCommandLineCodeExecutor(timeout=30)
executor_agent = ConversableAgent(
    name="executor",
    system_message="Execute Python code and return results.",
    code_execution_config={"executor": code_executor},
    human_input_mode="NEVER"
)

# Initialize Group Chat and Manager
group_chat = GroupChat(
    agents=[assistant, executor_agent],
    messages=[],
    max_round=6,
    speaker_selection_method="round_robin"
)

manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=assistant.llm_config
)

# Function to extract Python code from assistant's response
def extract_python_code(response):
    """Extract Python code from a response string."""
    patterns = [
        r'```python\n(.*?)\n```',  # Standard markdown
        r'```\n(.*?)\n```',        # Code block without language
        r'%%\n(.*?)\n%%',          # Alternative block format
        r'"""(.*?)"""',            # Triple-quoted string
        r"'''(.*?)'''"             # Triple-single-quoted string
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response, re.DOTALL)
        if match:
            code = match.group(1).strip()
            if code.startswith('python'):
                code = code[6:].lstrip()
            return code
    return None

# Streamlit UI setup
st.set_page_config(page_title="SFDC Brewery Salesforce Developer Agent", page_icon=":robot_face:", layout="wide")
st.title("SFDC Brewery Salesforce Developer Agent 🤖")
st.markdown("Welcome! Describe your JIRA task below, and I'll generate and execute the corresponding Salesforce code for you.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Describe your Salesforce task:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Initiate chat with the manager
                chat_result = assistant.initiate_chat(
                    recipient=manager,
                    message=prompt
                )

                # Collect all assistant responses
                assistant_responses = [msg for msg in chat_result.chat_history if msg['name'] == 'assistant']
                
                # Try all responses until we find valid code
                python_code = None
                for response in reversed(assistant_responses):
                    python_code = extract_python_code(response['content'])
                    if python_code:
                        break

                if python_code:
                    st.code(python_code, language="python")
                    
                    # Execute the code
                    execution_result = executor_agent.initiate_chat(
                        recipient=manager,
                        message=python_code
                    )
                    
                    # Collect execution output
                    execution_output = ""
                    for msg in execution_result.chat_history:
                        if msg['name'] == 'executor':
                            execution_output += msg['content'] + "\n"
                    
                    # Display results
                    st.subheader("Execution Result:")
                    if execution_output.strip():
                        st.text(execution_output)
                    else:
                        st.warning("No output was returned from the code execution.")
                else:
                    st.error("No valid Python code generated")
                    st.text("Assistant responses for debugging:")
                    st.json([r['content'] for r in assistant_responses])
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
