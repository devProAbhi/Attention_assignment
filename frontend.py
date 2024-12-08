import streamlit as st
import ollama

# Initialize the Ollama client
client = ollama.Client()

# Function to get a response from Llama 3.2
def get_llama_response(prompt):
    response = client.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.message.content

# Streamlit app configuration
st.set_page_config(page_title="One-Day Trip Planner", layout="wide")
st.markdown(
    """
    <style>
    .assistant {
        background-color: #f9f9f9;
        color: #333;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        max-width: 80%;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    }
    .user {
        background-color: #d1f1ff;
        color: #333;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    }
    .chat-container {
        overflow-y: auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 10px;
        background-color: #ffffff;
    }
    .input-container {
        display: flex;
        gap: 10px;
        margin-top: 10px;
        align-items: center;
    }
    .text-input {
        flex: 1;
        height: 45px;
        padding: 5px 10px;
        font-size: 16px;
        border: 1px solid #ccc;
        border-radius: 5px;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    }
    .send-button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
    }
    .send-button:hover {
        background-color: #0056b3;
    }
    .spinner-text {
        font-size: 14px;
        color: #888;
        margin-left: 10px;
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("One-Day Trip Planner")
st.write("Plan your perfect day trip with me!")

# Initialize session state for conversation and user input
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""
if 'is_typing' not in st.session_state:
    st.session_state['is_typing'] = False

# Function to handle sending the message
def send_message():
    user_input = st.session_state['user_input'].strip()
    if user_input:
        # Add user input to the conversation
        st.session_state['conversation'].append({"role": "user", "content": user_input})
        st.session_state['user_input'] = ""

        # Show "Assistant is typing..." near the Send button
        st.session_state['is_typing'] = True

        # Construct dynamic prompt based on conversation
        memory = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state['conversation']])
        prompt = f"""
        You are a friendly and professional tour planning assistant. Respond conversationally to help the user plan a one-day trip. Follow these guidelines:
        1. Ask questions to collect trip details like city, date, timing, budget, interests, and starting point, and note that you should ask follow-up questions step by step, not all at once.
        2. Dynamically create and update a detailed itinerary based on user preferences.
        3. Use follow-up questions to refine the plan and ensure user satisfaction.
        4. Provide clear and actionable outputs, including attraction details, travel methods, and costs.

        Conversation so far:
        {memory}

        Your Response:
        """
        # Get response from Llama 3.2
        response = get_llama_response(prompt)

        # Add assistant response to the conversation
        st.session_state['conversation'].append({"role": "assistant", "content": response})

        # Hide "Assistant is typing..." after response is received
        st.session_state['is_typing'] = False

# Display conversation
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state['conversation']:
    if msg['role'] == 'assistant':
        st.markdown(f"<div class='assistant'><b>Assistant:</b> {msg['content']}</div>", unsafe_allow_html=True)
    elif msg['role'] == 'user':
        st.markdown(f"<div class='user'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input box, Send button, and typing indicator
st.markdown('<div class="input-container">', unsafe_allow_html=True)
user_input = st.text_input(
    "",
    key="user_input",
    placeholder="Type your message here...",
    label_visibility="collapsed"
)
send = st.button("Send", on_click=send_message)

# Show typing indicator near the Send button
if st.session_state['is_typing']:
    st.markdown('<span class="spinner-text">Assistant is typing...</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
