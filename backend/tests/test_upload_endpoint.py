import requests
import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
import shutil
import uuid

# Determine the script's directory and the backend directory
script_dir = Path(__file__).resolve().parent
backend_dir = script_dir.parent

# URL for the backend service. Loaded from .env or defaults to localhost:8000
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
UPLOAD_ENDPOINT = f"{BACKEND_URL}/api/v1/upload"

# --- Load Actual PDF File ---
pdf_filename = "Muhsinun Chowdhury Resume.pdf"
pdf_file_path = os.path.join(script_dir, "assets", "example_pdfs", pdf_filename)

# Assume your FastAPI app is defined in app.main
# Adjust the import path if your app instance is located elsewhere
try:
    from app.main import app
except ImportError:
    # If running tests from a different structure, adjust path as needed
    import sys
    sys.path.insert(0, Path(__file__).resolve().parent.parent.as_posix())
    from app.main import app

# Determine the test upload directory from environment or use a default
TEST_UPLOAD_DIR_STR = os.getenv("UPLOAD_DIR", "/app/test_uploads")
TEST_UPLOAD_DIR = Path(TEST_UPLOAD_DIR_STR)

@pytest.fixture(scope="module")
def client():
    """Create a TestClient instance for the FastAPI app."""
    # Ensure the test upload directory exists and is clean before tests run
    if TEST_UPLOAD_DIR.exists():
        shutil.rmtree(TEST_UPLOAD_DIR)
    TEST_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Set the UPLOAD_DIR environment variable for the test session
    # This ensures the endpoint uses the test directory
    original_upload_dir = os.environ.get("UPLOAD_DIR")
    os.environ["UPLOAD_DIR"] = TEST_UPLOAD_DIR_STR

    with TestClient(app) as c:
        yield c

    # Clean up the test upload directory after tests run
    if TEST_UPLOAD_DIR.exists():
        shutil.rmtree(TEST_UPLOAD_DIR)

    # Restore original UPLOAD_DIR environment variable if it existed
    if original_upload_dir is None:
        # Use pop to avoid KeyError if it wasn't set initially
        os.environ.pop("UPLOAD_DIR", None)
    else:
        os.environ["UPLOAD_DIR"] = original_upload_dir

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

def test_upload_success(client: TestClient):
    """Test successful file upload using a real PDF file."""
    test_filename = "NIPS-2017-attention-is-all-you-need-Paper.pdf"
    # Construct the path relative to this test file's location
    script_dir = Path(__file__).resolve().parent
    pdf_file_path = script_dir / "assets" / "example_pdfs" / test_filename

    if not pdf_file_path.is_file():
        pytest.fail(f"Test PDF file not found at expected path: {pdf_file_path}")

    try:
        # Read the file content first for assertion later
        with open(pdf_file_path, "rb") as f_read:
            file_content_original = f_read.read()

        # Open the file again for uploading
        with open(pdf_file_path, "rb") as f_upload:
            files = {'file': (test_filename, f_upload, 'application/pdf')}

            response = client.post("/api/v1/upload", files=files)

    except Exception as e:
        pytest.fail(f"An error occurred during file preparation or upload: {e}")

    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert data["original_filename"] == test_filename
    assert data["content_type"] == 'application/pdf'
    assert data["file_id"].startswith("file_")

    # Verify the file was actually saved in the test directory and matches the original content
    file_id = data["file_id"]
    expected_path = TEST_UPLOAD_DIR / f"{file_id}.pdf"
    assert expected_path.exists()
    assert expected_path.read_bytes() == file_content_original

def test_upload_no_filename(client: TestClient):
    """Test uploading a file without providing a filename."""
    # Sending None as filename to TestClient (supported way)
    files = {'file': (None, b"some content", "application/octet-stream")}
    response = client.post("/api/v1/upload", files=files)

    # Expecting a 422 Unprocessable Entity if Starlette/FastAPI handles it first
    # Or 400 Bad Request if it reaches our endpoint logic check (less likely with TestClient)
    assert response.status_code == 422 # FastAPI/Starlette validation usually catches this
    # Detail message might vary, but check for relevance
    detail = response.json().get("detail", [])
    assert isinstance(detail, list)
    assert len(detail) > 0
    assert any("file" in item.get("loc", []) for item in detail) # Check that the error is related to the 'file' field

# Optional: Add a test for incorrect field name if desired
# def test_upload_wrong_field_name(client: TestClient):
#     test_filename = "wrong_field.txt"
#     file_content = b"content"
#     files = {'wrong_field': (test_filename, file_content, 'text/plain')}
#     response = client.post("/api/v1/upload", files=files)
#     assert response.status_code == 422 # Unprocessable Entity due to missing 'file' field

if __name__ == "__main__":
    test_upload() 