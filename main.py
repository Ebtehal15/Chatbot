import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import os

from langchain_community.chat_models import ChatOpenAI

from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

def init():
    load_dotenv()
    # Load the OpenAI API key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(
        page_title="Chat with Me",
        page_icon="🤖"
    )

def main():
    init()

    chat = ChatOpenAI(temperature=0)

    # Initialize messages if not present
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant."),
        ]

    st.header("istediginiz soruyu sorabilirisiniz 🤖")
    with st.sidebar:
        user_input = st.text_input("Your message:", key="user_input")

    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        # Send the message history to our chat
        with st.spinner("Düşünüyor"):
            response = chat(st.session_state.messages)

        # Correct the line below to use 'messages' instead of 'message'
        st.session_state.messages.append(AIMessage(content=response.content))

    # Retrieve the messages from session state
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):  # Start from 1 to skip the SystemMessage
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')

if __name__ == '__main__':
    main()
