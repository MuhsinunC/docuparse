# frontend/app.py
import streamlit as st
import os
import requests # Make sure 'requests' is in frontend/conda.yml
import logging

# Configure basic logging for the frontend too (optional)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
st.title("📄 DocuParse")

# Get backend URL from environment variable set in docker-compose.yml
backend_url = os.getenv("BACKEND_URL", "http://localhost:8000") # Default for local run

st.write(f"Connecting to backend at: {backend_url}")

# Simple check to see if backend is reachable
try:
    response = requests.get(f"{backend_url}/", timeout=5) # Added timeout
    response.raise_for_status() # Raise an exception for bad status codes
    st.success(f"Backend Connection Successful: {response.json().get('message', '')}")
except requests.exceptions.RequestException as e:
    st.error(f"Backend Connection Failed: {e}")

st.header("Upload Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("Filename:", uploaded_file.name)
    st.write("File type:", uploaded_file.type)
    st.write("File size:", uploaded_file.size, "bytes")

    # Button to trigger sending the file to the backend
    if st.button("Parse Document"):
        # Prepare the file for the POST request
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        parse_endpoint = f"{backend_url}/api/v1/parse/upload"

        st.info(f"Sending {uploaded_file.name} to {parse_endpoint}...")
        logger.info(f"Frontend: Sending {uploaded_file.name} to backend.")

        try:
            parse_response = requests.post(parse_endpoint, files=files, timeout=30) # Added timeout
            parse_response.raise_for_status()
            st.success("File sent successfully!")
            st.json(parse_response.json()) # Display backend response
        except requests.exceptions.RequestException as e:
            st.error(f"Error sending file to backend: {e}")
            if e.response:
                st.error(f"Backend response: {e.response.text}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

st.header("Results")
# Placeholder for displaying results - clear previous results on new upload/parse
if 'parse_result' in st.session_state:
    # Display logic here based on the structure of parse_result
    st.json(st.session_state.parse_result)
else:
    st.info("Parsing results will appear here.")