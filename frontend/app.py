# frontend/app.py
import streamlit as st
import os
import requests # Make sure 'requests' is in frontend/conda.yml

st.set_page_config(layout="wide")
st.title("📄 DocuParse")

# Get backend URL from environment variable set in docker-compose.yml
backend_url = os.getenv("BACKEND_URL", "http://localhost:8000") # Default for local run without docker-compose

st.write(f"Connecting to backend at: {backend_url}")

# Simple check to see if backend is reachable
try:
    response = requests.get(f"{backend_url}/")
    response.raise_for_status() # Raise an exception for bad status codes
    st.success(f"Backend Connection Successful: {response.json().get('message', '')}")
except requests.exceptions.RequestException as e:
    st.error(f"ERROR: Backend Connection Failed: {e}")

st.header("Upload Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("Filename:", uploaded_file.name)
    st.write("File type:", uploaded_file.type)
    st.write("File size:", uploaded_file.size, "bytes")

    # Placeholder for sending file to backend
    if st.button("Parse Document"):
        st.info("Parsing functionality not yet implemented.")
        # files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        # try:
        #     # Adjust endpoint as needed, e.g., /api/v1/parse/upload
        #     parse_response = requests.post(f"{backend_url}/parse", files=files)
        #     parse_response.raise_for_status()
        #     st.success("File sent for parsing!")
        #     st.json(parse_response.json())
        # except requests.exceptions.RequestException as e:
        #     st.error(f"Error sending file to backend: {e}")
        # except Exception as e:
        #     st.error(f"An unexpected error occurred: {e}")

st.header("Results")
st.info("Parsing results will appear here.")
# Placeholder for displaying results