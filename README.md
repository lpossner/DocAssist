# DocAssist

> An AI-powered assistant for documenting and retrieving technical information in operative industrial environments

DocAssist is a Flask-based web application that combines voice recording, document management, and AI-powered question answering to help industrial workers quickly access and document technical information in the field.

## Features

### Voice-to-Text Recording
- Real-time audio recording with automatic speech-to-text transcription
- Uses faster-whisper (optimized Whisper implementation) for accurate transcription
- Quality filtering based on confidence scores and speech detection

### Document Management
- **User Documents**: Store and retrieve custom text documents
- **PDF Documents**: Upload technical manuals and documentation
- Intelligent PDF parsing with automatic chapter detection and bookmarks
- Vector-based semantic search using ChromaDB

### AI Question Answering
- Ask questions in natural language and get answers from your documents
- Streams responses in real-time using Server-Sent Events (SSE)
- Combines information from both user documents and PDF literature
- Automatic page number citations from PDF sources
- Prioritizes user-added information over literature when relevant

## Architecture

```
┌──────────────────┐
│  Web Frontend    │  (static/index.html)
│  - Voice Input   │
│  - Q&A Interface │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Flask Server    │  (server.py)
│  REST API        │
└────────┬─────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌──────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐
│  Whisper │ │ Vector │ │  PDF    │ │  Local   │
│  Model   │ │   DB   │ │  Parser │ │  LLM     │
└──────────┘ └────────┘ └─────────┘ └──────────┘
```

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) - Fast Python package installer and resolver
- Local LLM server running on `http://localhost:1234` (e.g., LM Studio)
- Audio input device for voice recording

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd docassist
```

2. Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install dependencies using uv:
```bash
uv sync
```

This will automatically:
- Create a virtual environment
- Install all required dependencies (Flask, ChromaDB, faster-whisper, sounddevice, numpy, PyMuPDF, tqdm, requests)
- Use the correct Python version (3.10)

4. Create necessary directories:
```bash
mkdir uploads
```

5. Set up a local LLM server:
   - Install [LM Studio](https://lmstudio.ai/) or similar
   - Load the an LLM of your choice
   - Start the server on port 1234

## Usage

### Starting the Server

```bash
uv run python server.py
```

Or activate the virtual environment first:
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python server.py
```

The application will be available at `http://localhost:5000`

### API Endpoints

#### Questions
- `POST /ask` - Submit a question
- `GET /stream` - Stream AI answer with SSE

#### Voice Recording
- `POST /start_recording` - Start audio recording
- `POST /stop_recording` - Stop recording and transcribe

#### Document Management
- `GET /documents` - Retrieve all user documents
- `POST /documents` - Add new documents
- `DELETE /documents` - Delete all documents
- `GET /documents/query` - Query documents by text

#### PDF Management
- `GET /pdf_documents` - Retrieve all PDF documents
- `POST /pdf_documents` - Upload a PDF file
- `GET /pdf_documents/query` - Query PDF documents by text

## How It Works

### 1. Speech-to-Text ([speech_to_text.py](speech_to_text.py))
- Captures audio at 16kHz using `sounddevice`
- Transcribes with faster-whisper (optimized Whisper implementation)
- Filters low-quality transcriptions automatically

### 2. PDF Processing ([pdf_parser.py](pdf_parser.py))
- Extracts text and bookmarks from PDFs using PyMuPDF
- Chunks content by chapters based on document structure
- Preserves page numbers and hierarchical titles

### 3. Vector Database ([vector_database.py](vector_database.py))
- Uses ChromaDB for semantic search
- Maintains separate collections for user docs and PDFs
- Enables fast retrieval of relevant information

### 4. AI Integration ([server.py](server.py))
- Queries both document collections for relevant context
- Constructs system prompt with retrieved information
- Streams responses from local LLM
- Includes page citations in answers

## Configuration

### LLM Server
Edit the following constants in [server.py](server.py):
```python
LLM_API_URL = "http://localhost:1234/api/v0/chat/completions"
```

### Model Selection
Change the faster-whisper model size in [speech_to_text.py](speech_to_text.py):
```python
# Options: tiny, base, small, medium, large-v2, large-v3
model = WhisperModel("small", device="cpu", compute_type="int8")
```

### Upload Directory
Modify the upload path in [server.py](server.py):
```python
UPLOAD_FOLDER = "uploads"
```

## Use Cases

- **Industrial Maintenance**: Document equipment issues and quickly retrieve repair procedures
- **Technical Support**: Access product manuals and troubleshooting guides hands-free
- **Field Operations**: Capture observations via voice and query historical records
- **Training**: Help new workers find answers in technical documentation

## Limitations

- Requires local LLM server (not included)
- PDF parsing works best with properly structured documents with bookmarks
- Voice transcription quality depends on audio input quality
- English language is prioritized for transcription

## License

This project is provided as-is for use in industrial documentation scenarios.

## Contributing

Contributions are welcome. Please ensure all changes maintain compatibility with the existing API structure and include appropriate error handling.
