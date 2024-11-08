import streamlit as st

def main():
    # Set the title for the home page
    st.title("Welcome to Fork & Fable")

    # Provide an introductory text for the user
    st.markdown("""
    
    You can choose between the following options:
    - **Admin Panel**: Manage the restaurant menu (add, edit, delete items)
    - **Chatbot**: Interact with our bot to place an order.
    """)

    # Sidebar for navigation
    page = st.sidebar.radio("Select a page", ("Home", "Admin Panel", "Chatbot"))

    # Handle navigation
    if page == "Admin Panel":
        # Import admin page function and call it
        import admin
        admin.admin_page()
    
    elif page == "Chatbot":
        # Import chatbot page function and call it
        import chatbot
        chatbot.main()

if __name__ == "__main__":
    main()
