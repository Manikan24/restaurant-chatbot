import streamlit as st

def main():
    # Custom CSS for improved visuals
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 3rem;
            font-weight: bold;
            color: #4F8BF9;
            text-align: center;
            margin-bottom: 0.5em;
        }
        .intro-box {
            background: #f0f2f6;
            border-radius: 12px;
            padding: 1.5em 2em;
            margin-bottom: 2em;
            box-shadow: 0 2px 8px rgba(79,139,249,0.08);
        }
        .sidebar .sidebar-content {
            background: #eaf1fb;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="main-title">🍴 Welcome to <span style="color:#F97C4F;">Fork & Fable</span>!</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="intro-box">'
        '<h4>How can we help you today?</h4>'
        '<ul>'
        '<li><b>Admin Panel</b>: Manage the restaurant menu (add, edit, delete items)</li>'
        '<li><b>Chatbot</b>: Interact with our bot to place an order.</li>'
        '</ul>'
        '</div>',
        unsafe_allow_html=True
    )

    # Sidebar for navigation with icons
    st.sidebar.image("https://img.icons8.com/color/96/restaurant.png", width=64)
    st.sidebar.markdown("## Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ("Home", "Admin Panel", "Chatbot"),
        format_func=lambda x: {
            "Home": "🏠 Home",
            "Admin Panel": "🛠️ Admin Panel",
            "Chatbot": "🤖 Chatbot"
        }[x]
    )

    # Handle navigation
    if page == "Admin Panel":
        import admin
        admin.admin_page()
    elif page == "Chatbot":
        import chatbot
        chatbot.main()
    else:
        st.info("Select a page from the sidebar to get started.")

if __name__ == "__main__":
    main()
