import streamlit as st
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

def init():
    load_dotenv()
    # Load the OpenAI API key from Streamlit secrets or environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(
        page_title="Chatbot",
        page_icon="🤖"
    )

def main():
    init()

    # Set up the OpenAI client
    client = ChatOpenAI(temperature=0)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.you can just write up to 5 lines")
        ]

    # Display chat messages from history
    st.title("İstediğiniz soruyu sorabilirsiniz 🤖")
    for message in st.session_state.messages[1:]:  # Skip the system message
        with st.chat_message("user" if isinstance(message, HumanMessage) else "assistant"):
            st.markdown(message.content)

    # Accept user input
    if prompt := st.chat_input("Ne sormak istersiniz?"):
        # Add user message to chat history
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Assistant yazıyor..."):
                response = client(st.session_state.messages)
                assistant_message = AIMessage(content=response.content)
                st.markdown(assistant_message.content)

        # Add assistant response to chat history
        st.session_state.messages.append(assistant_message)

if __name__ == "__main__":
    main()
