import os
import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from google.generativeai.types import StopCandidateException

# Configure the API key
genai.configure(api_key="AIzaSyBn_f6WCEbDu_U-kOrYwP6vKkDKSZzwT1M")  # Replace with your actual API key

# Define the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)

# Function to start a chat session
def start_chat():
    return model.start_chat(
        history=[
            {
                "role": "model",
                "parts": [
                    "Hello! I'm D-CARE here to listen and offer support. How are you feeling today? 😊\n",
                ],
            }
        ]
    )

# Streamlit app
st.set_page_config(page_title="D-CARE", page_icon=":sunflower:", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
        color: #333;
        font-family: 'Arial', sans-serif;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
        padding: 10px;
    }
    .stButton > button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextArea > div > textarea {
        border-radius: 10px;
        padding: 10px;
    }
    .user-message {
        color: blue;
        font-weight: bold;
    }
    .ai-message {
        color: green;
        font-style: italic;
    }
    .error-message {
        color: red;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌼 Depression Comprehensive Assessment and Recognition Engine (D-CARE)")

st.header("Chat with D-CARE")

conversation_history = st.empty()

if 'conversation_log' not in st.session_state:
    st.session_state.conversation_log = [
        "D-CARE: Hello! I'm D-CARE here to listen and offer support. How are you feeling today? 😊"
    ]

if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

def display_conversation():
    formatted_conversation = ""
    for entry in st.session_state.conversation_log:
        if entry.startswith("You:"):
            formatted_conversation += f'<p class="user-message">{entry}</p>'
        elif entry.startswith("Error:"):
            formatted_conversation += f'<p class="error-message">{entry}</p>'
        else:
            formatted_conversation += f'<p class="ai-message">{entry}</p>'
    conversation_history.markdown(formatted_conversation, unsafe_allow_html=True)

def send_message():
    user_input = st.session_state.get(f'user_input_{st.session_state.input_key}', '')
    if user_input:
        # Append user input to conversation history
        st.session_state.conversation_log.append(f"You: {user_input}")
        
        try:
            # Send user input to the chat session
            response = chat_session.send_message(user_input)
            if response:
                # Append AI response to conversation history
                st.session_state.conversation_log.append(f"D-CARE: {response.text}")
            else:
                st.session_state.conversation_log.append("Error: No response received from the model.")
        
        except ResourceExhausted:
            st.session_state.conversation_log.append("Error: Sorry, the resource quota has been exhausted. Please try again later.")
        
        except StopCandidateException as e:
            st.session_state.conversation_log.append("Error: The response generated was flagged for safety. Please try a different input.")
        
        except Exception as e:
            st.session_state.conversation_log.append(f"Error: An unexpected error occurred: {str(e)}")

        # Clear the input box indirectly by updating the input key
        st.session_state.input_key += 1

    display_conversation()

# Initialize chat session
chat_session = start_chat()

# Display initial conversation
display_conversation()

# Input field for user message
user_input = st.text_input("You:", key=f"user_input_{st.session_state.input_key}")

# Button to send message
if st.button("Send"):
    send_message()
