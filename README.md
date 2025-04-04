# Pathway RAG Application

A powerful RAG (Retrieval-Augmented Generation) application built using Pathway, designed to provide intelligent question-answering capabilities with hybrid search functionality.

## Features

- **Hybrid Search**: Combines BM25 keyword-based search with vector-based semantic search for optimal results
- **Document Processing**: Supports various document formats with UnstructuredParser
- **Smart Chunking**: Token-based text splitting for efficient processing
- **Advanced Embeddings**: Uses GIST-small-Embedding-v0 for high-quality document embeddings
- **LLM Integration**: Powered by Gemini 2.5 Pro for generating responses
- **Caching**: Implements disk caching for improved performance
- **Docker Support**: Containerized deployment with Docker and Docker Compose

## Prerequisites

- Docker and Docker Compose
- Pathway license key
- Google Cloud credentials (if using Google Cloud services)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd pathway-rag
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Configuration

The application is configured through `app.yaml`. Key configuration options include:
- Document sources
- LLM model settings
- Embedding model selection
- Server host and port settings

## Usage

### Running with Docker Compose (Recommended)

1. Build and start the application:
```bash
docker-compose build
docker-compose up
```

The application will be available at `http://localhost:8000`.

### Alternative: Running Locally

If you prefer running locally without Docker:

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

## Project Structure

```
.
├── app.py                 # Main application file
├── app.yaml              # Configuration file
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── Cache/               # Cache directory
├── data/                # Data storage
├── newsfiles/          # News documents
└── ui/                  # User interface components
```

## Dependencies

- pathway[all]
- python-dotenv==1.0.1
- mpmath==1.3.0
- litellm>=1.35
- Google-generativeai
- Sentence-transformers

## License

This project requires a valid Pathway license key to use advanced features.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, please open an issue in the repository. 