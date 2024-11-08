import streamlit as st
import json
from database import create_db, store_menu_in_db, get_menu_from_db, get_categories_from_db, update_item_in_db, delete_item_from_db, add_item_to_db

def admin_page():
    st.title('Admin - Manage Menu')

    # Option to upload JSON file
    uploaded_file = st.file_uploader("Upload a JSON file with the menu", type="json")
    
    if uploaded_file is not None:
        menu_data = json.load(uploaded_file)
        store_menu_in_db(menu_data)
        st.success('Menu uploaded and stored in database!')

    st.subheader("Manage Items")

    # Fetch categories and items from the database
    menu = get_menu_from_db()
    categories = get_categories_from_db()

    # Option to view, edit, or delete items
    action = st.selectbox("Choose action", ["View Menu", "Edit Item", "Delete Item", "Add New Item"])

    if action == "View Menu":
        st.write("**Menu Items**")
        for category_name, item_id, item_name, item_description, item_price, item_availability in menu:
            st.write(f"Category: {category_name}")
            st.write(f"Item: {item_name}")
            st.write(f"Description: {item_description}")
            st.write(f"Price: {item_price}")
            st.write(f"Availability: {item_availability}")
            st.write("---")
    
    elif action == "Edit Item":
        item_to_edit = st.selectbox("Select an item to edit", [f"{item_name} ({item_id})" for category_name, item_id, item_name, _, _, _ in menu])
        item_id = int(item_to_edit.split("(")[-1][:-1])  # Extract item_id from the selection
        
        item_details = next(item for item in menu if item[1] == item_id)
        item_name = st.text_input("Item Name", item_details[2])
        item_description = st.text_area("Item Description", item_details[3])
        item_price = st.number_input("Price", min_value=0.0, value=item_details[4])
        item_availability = st.number_input("Availability", min_value=0, value=item_details[5])
        category_id = st.selectbox("Category", [category[0] for category in categories])

        if st.button("Update Item"):
            update_item_in_db(item_id, item_name, item_description, item_price, item_availability, category_id)
            st.success("Item updated successfully!")
    
    elif action == "Delete Item":
        item_to_delete = st.selectbox("Select an item to delete", [f"{item_name} ({item_id})" for category_name, item_id, item_name, _, _, _ in menu])
        item_id = int(item_to_delete.split("(")[-1][:-1])  # Extract item_id from the selection
        
        if st.button("Delete Item"):
            delete_item_from_db(item_id)
            st.success("Item deleted successfully!")
    
    elif action == "Add New Item":
        item_name = st.text_input("Item Name")
        item_description = st.text_area("Item Description")
        item_price = st.number_input("Price", min_value=0.0)
        item_availability = st.number_input("Availability", min_value=0)
        category_id = st.selectbox("Category", [category[0] for category in categories])

        if st.button("Add Item"):
            add_item_to_db(item_name, item_description, item_price, item_availability, category_id)
            st.success("Item added successfully!")

