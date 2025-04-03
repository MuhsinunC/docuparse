import requests
import io
import os
from dotenv import load_dotenv
from pathlib import Path

# Determine the script's directory and the backend directory
script_dir = Path(__file__).resolve().parent
backend_dir = script_dir.parent

# Load environment variables from .env file in the backend directory
dotenv_path = backend_dir / '.env'
if dotenv_path.exists():
    print(f"Loading environment variables from: {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}. Using default or system env vars.")

# URL for the backend service. Loaded from .env or defaults to localhost:8000
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
UPLOAD_ENDPOINT = f"{BACKEND_URL}/api/v1/parse/upload"

# --- Load Actual PDF File ---
pdf_filename = "Muhsinun Chowdhury Resume.pdf"
pdf_file_path = os.path.join(script_dir, "assets", "example_pdfs", pdf_filename)

def test_upload():
    print(f"--- Testing Upload Endpoint ({UPLOAD_ENDPOINT}) ---")

    if not os.path.isfile(pdf_file_path):
        print(f"\nTest Failed: PDF file not found at {pdf_file_path}")
        print("Please place the resume PDF in the backend/tests/ directory.")
        print("--- Test Finished ---")
        return

    print(f"Using PDF file: {pdf_file_path}")

    try:
        # Open the actual PDF file in binary read mode
        with open(pdf_file_path, "rb") as f:
            # Prepare the file for the POST request
            files = {"file": (pdf_filename, f, "application/pdf")}

            response = requests.post(UPLOAD_ENDPOINT, files=files, timeout=30) # Increased timeout slightly
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

            print(f"Status Code: {response.status_code}")
            print("Response JSON:")
            try:
                response_json = response.json()
                print(response_json)
                # Check if the returned filename matches
                if response_json.get("filename") == pdf_filename:
                    print("\nTest Passed: Filename matched.")
                else:
                    print("\nTest Failed: Filename mismatch.")
            except requests.exceptions.JSONDecodeError:
                print("Response was not valid JSON.")
                print(f"Response Text: {response.text[:500]}...") # Print first 500 chars
                print("\nTest Failed: Invalid JSON response.")

    except requests.exceptions.ConnectionError as e:
        print(f"\nTest Failed: Connection Error. Is the backend running at {BACKEND_URL}? ({e})")
    except requests.exceptions.Timeout:
        print("\nTest Failed: Request timed out.")
    except FileNotFoundError:
         print(f"\nTest Failed: Could not find the PDF file at {pdf_file_path}") # Should be caught earlier, but good practice
    except requests.exceptions.RequestException as e:
        print(f"\nTest Failed: An unexpected request error occurred: {e}")
        if e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response text: {e.response.text[:500]}...")
    finally:
        print("--- Test Finished ---")

if __name__ == "__main__":
    test_upload() 