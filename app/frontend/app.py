import streamlit as st
import requests
import json

# Backend URL configuration
BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Prototype WebApp",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Prototype WebApp: Streamlit + FastAPI")
st.markdown("This is a simple proof of concept app blending Streamlit for the frontend and FastAPI for the backend.")

# Navigation
tab1, tab2 = st.tabs(["View Items", "Add New Item"])

with tab1:
    st.header("Items List")
    if st.button("Refresh Items"):
        try:
            response = requests.get(f"{BACKEND_URL}/items/")
            if response.status_code == 200:
                items = response.json().get("items", [])
                if items:
                    for item in items:
                        with st.expander(f"Item: {item['name']}"):
                            st.write(f"**ID:** {item['id']}")
                            st.write(f"**Description:** {item.get('description', 'N/A')}")
                            st.write(f"**Price:** ${item['price']}")
                else:
                    st.info("No items found. Go to 'Add New Item' to create some.")
            else:
                st.error("Failed to fetch items from the backend.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend. Is FastAPI running on port 8000?")

with tab2:
    st.header("Add a New Item")
    with st.form("new_item_form"):
        name = st.text_input("Name")
        description = st.text_area("Description")
        price = st.number_input("Price", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Create Item")
        
        if submitted:
            if not name:
                st.warning("Please enter a name for the item.")
            else:
                try:
                    payload = {"name": name, "description": description, "price": price}
                    response = requests.post(f"{BACKEND_URL}/items/", json=payload)
                    if response.status_code == 200:
                        st.success(f"Successfully created item '{name}'!")
                    else:
                        st.error(f"Failed to create item. Status Code: {response.status_code}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the backend. Is FastAPI running on port 8000?")

st.sidebar.markdown("### About")
st.sidebar.info(
    "This web application demonstrates a fast-paced development framework "
    "using *Streamlit* for rapid UI creation and *FastAPI* for a robust, "
    "high-performance backend API."
)
st.sidebar.markdown("---")
st.sidebar.text("v0.1.0")
