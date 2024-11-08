import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from database import get_menu_from_db, get_categories_from_db  # Importing database functions

# Load environment variables from .env
project_root = Path(__file__).resolve().parent
load_dotenv(project_root / ".env")

class GroqAPI:
    """Handles API interactions with Groq for generating chat responses."""
    def __init__(self, model_name="llama3-8b-8192"):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = model_name

    def _response(self, message):
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=message,
            temperature=0,
            max_tokens=4096,
            stream=True,
            stop=None,
        )

    def response_stream(self, message):
        response = ""
        for chunk in self._response(message):
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
        return response

class Message:
    """Manages chat messages within the Streamlit UI."""
    def __init__(self):
        # Fetch the menu from the database to create the system prompt
        menu = get_menu_from_db()
        categories = get_categories_from_db()

        # Build the menu content dynamically from the database
        menu_content = "# Menu\n\n"
        current_category = None
        for category_name, item_id, item_name, item_description, item_price, item_availability in menu:
            if category_name != current_category:
                if current_category:
                    menu_content += "\n"  # Add a newline between categories
                menu_content += f"## {category_name}\n"
                current_category = category_name
            menu_content += f"- {item_name}: {item_description} - ${item_price} ({'Available' if item_availability else 'Out of Stock'})\n"

        self.system_prompt = f"""
             You are MenuMaster, an automated assistant for placing orders at an online restaurant.
    Start by greeting the customer, then gather their order. 
    After collecting the full order, summarize it and confirm if they want to add anything else.
    Ask if it’s a dine-in or online order after finalizing the order.
    maintain in Indian rupees.
    For delivery orders, request the delivery address. 
    Keep your responses brief, friendly, and conversational.
    Note: Double-check your calculations before asking for the final payment.
    Note: Show the cart or order properly with quantity and price.

    IMPORTANT: If the message is not related to placing an order (like code or general things), do not respond.
    Only respond to messages that are related to the order process.
    Finally, collect the payment.
        
        {menu_content}
        """
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": self.system_prompt}]

    def add(self, role: str, content: str):
        st.session_state.messages.append({"role": role, "content": content})

    def display_chat_history(self):
        for message in st.session_state.messages:
            if message["role"] == "system":
                continue
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def display_response(self, response):
        with st.chat_message("assistant"):
            st.markdown(response)

# Entry point for the Streamlit app
def main():
    # Get user input through the Streamlit chat input
    user_input = st.chat_input("Enter your order or message...")

    # Create a Message object to manage chat history
    message = Message()

    # If there's user input, process it through the default "llama" model
    if user_input:
        llm = GroqAPI()  # Default model llama3-8b-8192
        message.add("user", user_input)  # Add user input to session state
        message.display_chat_history()  # Display the chat history
        response = llm.response_stream(st.session_state.messages)  # Get the complete response
        message.add("assistant", response)  # Add assistant's response to session state
        message.display_response(response)  # Display the assistant's response in chat

if __name__ == "__main__":
    main()
