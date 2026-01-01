# DocAssist

> An AI-powered assistant for documenting and retrieving technical information in operative industrial environments

DocAssist is a Flask-based web application that combines voice recording, document management, and AI-powered question answering to help industrial workers quickly access and document technical information in the field.

## Features

### Voice-to-Text Recording
- Real-time audio recording with automatic speech-to-text transcription
- Uses OpenAI's Whisper model for accurate transcription
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
┌─────────────────┐
│  Web Frontend   │  (static/index.html)
│  - Voice Input  │
│  - Q&A Interface│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flask Server   │  (server.py)
│  REST API       │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬─────────────┐
    ▼         ▼          ▼             ▼
┌────────┐ ┌──────┐ ┌─────────┐ ┌──────────┐
│Whisper │ │Vector│ │  PDF    │ │Local LLM │
│ Model  │ │  DB  │ │ Parser  │ │(Mistral) │
└────────┘ └──────┘ └─────────┘ └──────────┘
```

## Prerequisites

- Python 3.8+
- Local LLM server running on `http://localhost:1234` (e.g., LM Studio with Mistral Nemo)
- Audio input device for voice recording

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd docassist
```

2. Install required dependencies:
```bash
pip install flask chromadb openai-whisper sounddevice numpy PyMuPDF tqdm requests
```

3. Create necessary directories:
```bash
mkdir uploads
```

4. Set up a local LLM server:
   - Install [LM Studio](https://lmstudio.ai/) or similar
   - Load the Mistral Nemo Instruct 2407 model
   - Start the server on port 1234

## Usage

### Starting the Server

```bash
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
- Transcribes with Whisper "small" model
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
Change the Whisper model size in [speech_to_text.py](speech_to_text.py):
```python
model = whisper.load_model("small", in_memory=True)  # Options: tiny, base, small, medium, large
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
