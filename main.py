import logging
import os
from typing import List
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Set up logging to display information in the console.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


load_dotenv()

# Setting up OpenAI API
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"))


def generate_response(messages: List[dict]) -> str:
    try:
        logger.info(f"Generating response for message: {messages[-1]['content']}")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        response_content = response.choices[0].message.content.strip()
        logger.info(f"Response generated successfully: {response_content[:100]}...")
        return response_content

    except Exception as e:
        error_msg = f"Error in generate_response: {str(e)}"
        logger.error(error_msg)
        return f"Error: {str(e)}"


def initialize_session_state():
    try:
        if "messages" not in st.session_state:
            logger.info("Initializing new session state")
            st.session_state.messages = [
                {"role": "system",
                 "content": "You are a helpful and friendly assistant. Your goal is to assist the user by providing accurate, useful, and well-structured answers. Explain clearly and concisely, avoiding overly complex terminology. When appropriate, offer additional tips or suggestions to help the user achieve their goals."}
            ]
            # Add initial greeting message
            st.session_state.messages.append(
                {"role": "assistant", "content": "Hi! How can I help you?"}
            )
            logger.info("Session state initialized with greeting message")
    except Exception as e:
        logger.error(f"Error in initialize_session_state: {str(e)}")


def main():
    try:
        logger.info("Starting application")
        st.title("🤖 AI ChatBot")

        # Initialize session state
        initialize_session_state()

        # Display chat history
        for message in st.session_state.messages[1:]:  # Skip the system prompt
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # User input message
        if prompt := st.chat_input("Enter your message"):
            logger.info(f"Received user input: {prompt}")

            # Adding a user message to history
            st.session_state.messages.append(
                {"role": "user", "content": prompt}
            )
            logger.info("User message added to session state")

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generating and displaying the response
            with st.chat_message("assistant"):
                with st.spinner("Generating response..."):
                    response = generate_response(st.session_state.messages)
                    st.markdown(response)
                    logger.info("Response displayed to user")

            # Adding a reply to the story
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
            logger.info("Assistant response added to session state")

    except Exception as e:
        logger.error(f"Error in main function: {str(e)}")
        st.error("An error occurred in the application. Please check the logs for details.")


if __name__ == "__main__":
    main()
