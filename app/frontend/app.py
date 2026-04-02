import streamlit as st
import requests
import json
import os

# Backend URL configuration
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Prototype WebApp",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Prototype WebApp: Streamlit + FastAPI")
st.markdown("This is a simple proof of concept app blending Streamlit for the frontend and FastAPI for the backend.")

# Initialize session state for items
if "items" not in st.session_state:
    st.session_state["items"] = []

def fetch_items():
    try:
        response = requests.get(f"{BACKEND_URL}/items/")
        if response.status_code == 200:
            st.session_state["items"] = response.json().get("items", [])
            st.success("Items list refreshed!")
        else:
            st.error("Failed to fetch items from the backend.")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend. Is FastAPI running on port 8000?")

# Navigation
tab1, tab2 = st.tabs(["View Items", "Add New Item"])

with tab1:
    st.header("Items List")
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Refresh Items"):
            fetch_items()

    if st.session_state["items"]:
        for item in st.session_state["items"]:
            with st.expander(f"Item: {item['name']}"):
                st.write(f"**ID:** {item['id']}")
                st.write(f"**Description:** {item.get('description', 'N/A')}")
                st.write(f"**Price:** ${item['price']}")
                
                # Using key= ensures Streamlit knows which button is being tracked
                if st.button("Item Analysis", key=f"analyze_{item['id']}"):
                    try:
                        # Calling the new WebApp backend analysis endpoint 
                        analysis_response = requests.get(f"{BACKEND_URL}/items/{item['id']}/analyze")
                        if analysis_response.status_code == 200:
                            analysis = analysis_response.json()
                            if analysis:
                                st.markdown("---")
                                st.subheader("📊 Engine Analysis")
                                acol1, acol2 = st.columns(2)
                                with acol1:
                                    st.metric("Popularity Score", analysis.get("popularity_score", "N/A"))
                                    st.write(f"**Trend:** {analysis.get('last_market_trend', 'N/A')}")
                                with acol2:
                                    st.write(f"**Restock Priority:** {analysis.get('restock_priority', 'N/A')}")
                                    st.write(f"**Engine Used:** {analysis.get('python_engine', 'N/A')}")
                            else:
                                st.info("Analysis was empty for this item.")
                        else:
                            st.error(f"Failed to fetch analysis. Code: {analysis_response.status_code}")
                    except requests.exceptions.ConnectionError:
                        st.error("Error connecting to WebApp backend.")
    else:
        st.info("No items found. Click 'Refresh Items' or add a new one.")

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
                        # Trigger a refresh after creation
                        fetch_items()
                        st.rerun()
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
