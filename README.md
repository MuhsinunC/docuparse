# DocuParse Project

This project is a full-stack application for parsing documents (initially PDFs) and extracting structured information.
It features a backend API for processing and a Streamlit frontend for user interaction, orchestrated via Docker Compose.

## Project Structure

```
docuparse/
├── backend/                  # FastAPI Backend API Service
│   ├── app/                  # Core application logic
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app definition and root endpoints
│   │   ├── api/              # API endpoint definitions
│   │   │   ├── __init__.py
│   │   │   └── v1/           # API version 1
│   │   │       ├── __init__.py
│   │   │       ├── routes.py     # Central router for v1 endpoints
│   │   │       └── endpoints/    # Logic for individual API endpoints
│   │   │           ├── __init__.py
│   │   │           ├── upload.py   # Upload endpoint logic
│   │   │           ├── parse.py    # Parse endpoint logic
│   │   │           ├── extract.py  # Extract endpoint logic
│   │   │           ├── split.py    # Split endpoint logic
│   │   │           ├── webhooks.py # Webhook endpoint logic
│   │   │           └── jobs.py     # Job status endpoint logic
│   │   ├── core/             # Core logic (parsing, structuring - if not in endpoints)
│   │   │   ├── __init__.py
│   │   │   ├── config.py     # Configuration settings
│   │   │   ├── parser.py     # Document parsing logic (if separated)
│   │   │   └── structurer.py # Logic to structure parsed data (if separated)
│   │   ├── models/           # Pydantic models for request/response
│   │   │   ├── __init__.py
│   │   │   └── document.py
│   │   └── schemas/          # Data schemas (if needed, e.g., for DB)
│   │       ├── __init__.py
│   │       └── ...
│   ├── tests/                # Backend tests
│   │   ├── __init__.py
│   │   └── ...
│   ├── Dockerfile            # Dockerfile for the backend service
│   ├── conda.yml             # Conda dependencies for the backend
│   └── .env                  # Backend environment variables (Create from .env.example)
│   └── .env.example          # Example backend environment variables
│
├── frontend/                 # Streamlit Frontend Service
│   ├── app.py                # Main Streamlit application script
│   ├── pages/                # Optional: For multi-page Streamlit apps
│   │   └── ...
│   ├── components/           # Reusable UI components (optional)
│   │   └── ...
│   ├── utils/                # Utility functions (e.g., API client)
│   │   └── api_client.py
│   ├── Dockerfile            # Dockerfile for the frontend service
│   ├── conda.yml             # Conda dependencies for the frontend
│   └── .env                  # Frontend environment variables (Create from .env.example)
│   └── .env.example          # Example frontend environment variables
│
├── docker-compose.yml        # Docker Compose configuration
├── .gitignore                # Git ignore file
└── README.md                 # Project specification (this file)
```

## Key Components

*   **`backend/`**: Contains the FastAPI application.
    *   `app/main.py`: Initializes the FastAPI app.
    *   `app/api/v1/routes.py`: Defines the APIv1 routes and maps them to endpoint logic files.
    *   `app/api/v1/endpoints/`: Contains the implementation logic for each API endpoint.
*   **`frontend/`**: Contains the Streamlit application, UI components, API client utilities, and its Dockerfile.
*   **`docker-compose.yml`**: Defines how to build and run the backend and frontend services together as containers. It uses the `.env` files within the `backend` and `frontend` directories.
*   **`.env` / `.env.example`**: Each service (`backend`, `frontend`) has its own environment configuration files. Copy `.env.example` to `.env` within each service directory and fill in your secrets/configurations.
*   **`README.md`**: The detailed specification for this project.

## Getting Started

1.  **Environment Setup**:
    *   Navigate to the `backend` directory, copy `backend/.env.example` to `backend/.env`, and fill in any required backend environment variables (e.g., API keys).
    *   Navigate to the `frontend` directory, copy `frontend/.env.example` to `frontend/.env`, and fill in any required frontend environment variables.
2.  **Run with Docker**:
    *   From the project root directory, run: `docker-compose up --build`
    *   The frontend should be accessible at `http://localhost:8501`.
    *   The backend API docs should be accessible at `http://localhost:8000/docs`.

(Further instructions to be added later)

## 1. Goal

Develop a full-stack application, for data ingestion and advanced document parsing. Implement robust text and table extraction to address common, difficult PDF parsing challenges. Emphasis on handling complex layouts and accurate table structure.

The application will feature a backend API responsible for parsing documents and a separate Streamlit frontend for user interaction. It will initially focus on parsing uploaded PDF documents, extracting text and structured data (like tables), and providing well-structured JSON output via the API. The design should consider future extensibility to handle a wider array of file types and incorporate techniques like vision-based parsing.

## 2. Core Functionality

The application will allow users to upload documents through a web interface. The backend will process these documents to:
1.  Extract raw text content.
2.  Identify and extract tabular data.
3.  (Bonus) Extract images.
4.  Structure the extracted content (text, tables, image data, metadata) into a coherent JSON format.
5.  Extract file metadata (author, creation date, page count).

## 3. Key Features

### 3.1. Document Upload & Management
*   **UI:** Streamlit-based interface.
*   **Functionality:**
    *   Allow users to upload one or more PDF files.
    *   Display a list of uploaded documents.
    *   Show processing status (e.g., "Uploading", "Parsing", "Ready", "Error").

### 3.2. PDF Parsing Engine
*   **Technology:** Python backend using libraries like `PyMuPDF` (fitz), `pdfplumber`, `pdfminer.six`, docTR, Tesseract, Mistral OCR, Google Document AI, or Google Cloud Vision API as our most naive/MVP OCR implementation until we implement our own.
*   **Functionality (Initial Focus: PDFs):**
    *   **Text Extraction:** Extract text content preserving basic layout information where possible (e.g., paragraph breaks).
    *   **Table Extraction:** Detect and extract tables into a structured format (e.g., list of lists or list of dictionaries). Handle multi-page tables if feasible.
    *   **Image Extraction (Bonus):** Extract embedded images from PDFs.
    *   **Metadata Extraction:** Extract basic file metadata (author, creation date, page count).

### 3.3. Content Structuring
*   **Functionality:**
    *   **JSON Output:** Consolidate extracted text, tables, (optional) image data, and metadata into a well-defined JSON object. Mimic a simplified structure similar to what a production API might return.

### 3.4. User Interface (Streamlit)
*   **Layout:** Clean and intuitive interface.
*   **Components:**
    *   File uploader.
    *   Document status display.
    *   Area to display extracted raw text.
    *   Formatted display for extracted tables (`st.dataframe`).
    *   Display area for the final JSON output (syntax-highlighted).
    *   (Optional) Display extracted images.

## 4. Technology Stack

*   **Backend Language:** Python 3.9+
*   **Backend API Framework:** FastAPI
*   **PDF Parsing:** Local libraries (`PyMuPDF`, `pdfplumber`, `pdfminer.six`, `docTR`, `Tesseract`)
*   **Web Framework/UI:** Streamlit
*   **Orchestration:** Docker, Docker Compose
*   **Dependencies:** Conda `conda.yml` (separate for backend and frontend)

## 5. Architecture Overview

This project will be structured as a multi-container application orchestrated using Docker Compose.

1.  **Backend API Service (Python/FastAPI):**
    *   Exposes endpoints mirroring the desired parsing/extraction functionality (e.g., Upload, Parse, Extract).
    *   API routes are centrally defined in `app/api/v1/routes.py`.
    *   Logic for each endpoint (e.g., handling uploads, calling parsing functions) is implemented in separate files within `app/api/v1/endpoints/`.
    *   May contain core parsing/structuring logic in `app/core/` or integrate calls to external services.
    *   Handles file storage (temporarily or persistently) and potentially asynchronous processing.
2.  **Frontend Service (Streamlit):**
    *   Provides the user interface (`app.py`).
    *   Handles file uploads from the user.
    *   Makes HTTP requests to the Backend API Service to initiate parsing and fetch results.
    *   Displays processing status and the final structured data received from the API.
3.  **Docker Compose:** Defines and manages the multi-container setup (backend, frontend), loading environment variables from service-specific `.env` files.

## 6. UI/UX Description

*   **Main Page:** Title, brief description, file uploader widget.
*   **Processing View:** Upon upload, display progress indicators.
*   **Results View (per document):**
    *   Tabs or expandable sections for:
        *   "Raw Text"
        *   "Extracted Tables" (displaying each table)
        *   (Optional) "Extracted Images"
        *   "JSON Output" (syntax-highlighted)

## 7. Data Flow

1.  User uploads PDF via Streamlit UI (Frontend Service).
2.  Frontend Service sends the file data via an HTTP POST request to the Backend API Service's `/api/v1/upload` endpoint.
3.  Backend API Service (`upload.py`) receives the file, potentially stores it, and returns an identifier (e.g., upload ID or job ID).
4.  Frontend Service (or potentially the backend asynchronously) initiates parsing/extraction by calling appropriate backend endpoints (e.g., `/api/v1/parse`, `/api/v1/extract`) using the identifier from the upload step.
5.  Backend API Service endpoint logic (e.g., in `parse.py` or `extract.py`) handles the request, performs the core processing (potentially calling functions in `app/core` or external APIs), and might return a job ID for polling or send results via webhook.
6.  Frontend Service polls the Backend API Service (e.g., `/api/v1/jobs/{job_id}`) or listens for results (e.g., via WebSockets if implemented, or inferred through status updates).
7.  Backend API Service returns the processing status or the final JSON result via the relevant endpoint (e.g., job status or a dedicated results endpoint).
8.  Frontend Service receives the JSON and displays the extracted content in the Streamlit UI.

## 8. Evaluation / Success Metrics

*   **Functionality:** Successfully parses various test PDFs (simple text, complex layouts, tables). API endpoints behave as expected.
*   **Accuracy:** Extracted text is correct; tables are accurately identified and structured.
*   **Output Quality:** JSON output is well-formed and accurately represents the extracted content.
*   **UI/UX:** The Streamlit interface is intuitive and effectively displays results.
*   **Code Quality:** Code is well-organized (following the new structure), documented, follows Python best practices, and includes easy-to-replicate instructions for setting up the environment (Conda environments via `conda.yml`, Docker containers, `.env` files).
*   **Demonstration:** Ability to run the application locally and demonstrate its features effectively.

## 9. Potential Future Enhancements

*   Support for other document formats (e.g., .docx, .pptx, images).
*   Visual highlighting of extracted elements on a PDF preview (we might need to keep track of bounding boxes of the extracted elements to do this).
*   Implementing basic structured extraction based on user-defined schemas (e.g., extracting specific fields based on labels).
*   More sophisticated table detection and structure inference algorithms.
*   Integrating computer vision models (e.g., layout analysis, figure/chart understanding) for more robust parsing, especially for scanned documents or complex layouts.
*   Leveraging Large Language Models (LLMs) for Advanced Structured Extraction:
    *   Using LLM function calling or similar techniques to convert unstructured text/layout information into reliable structured JSON based on dynamic requirements or schemas.
    *   Exploring optimal chunking strategies and context formulation for feeding data to LLMs.
    *   Investigating parallel LLM calls on different document chunks to optimize inference speed.
    *   Utilizing multimodal LLMs to natively understand and extract information from text, tables, and embedded images/figures simultaneously.
*   Implementing asynchronous processing in the backend for large files (e.g., using Celery, FastAPI Background Tasks). This would allow us to scale across multiple compute resources.
*   Adding authentication/authorization to the API.
*   Adding configuration options for parsing (e.g., OCR settings, specific data types to extract).
*   Deployment to a cloud environment. This should be very easy given we designed the app to be containerized and scalable from the start.