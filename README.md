=======
# Authentic News Teller

A powerful news verification and question-answering system built using Pathway RAG (Retrieval-Augmented Generation) technology. This application helps users verify news authenticity and get accurate information from trusted news sources.

## Key Features

- **News Verification**: Intelligent system to help verify news authenticity and provide factual context
- **Smart News Processing**: Processes and analyzes news articles from various sources
- **Accurate Information Retrieval**: Uses hybrid search to find relevant news and facts
- **Real-time Answers**: Get immediate responses to questions about news articles
- **Source Verification**: Helps identify and validate news sources
- **Fact Cross-referencing**: Cross-references information across multiple news sources

## Technical Features

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
cd authentic-news-teller
```

2. Set up environment variables:
```bash
set up with pathway license key .env.example
set up files for accessing your google sheet, sheet id
# Edit .env with your configuration
```

## Configuration

The application is configured through `app.yaml`. Key configuration options include:
- News source directories and files
- LLM model settings for news analysis
- Embedding model selection
- Server host and port settings
- News processing parameters

## Usage

### Running with Docker Compose (Recommended)

1. Build and start the application:
```bash
docker compose build
docker compose up
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
├── Cache/               # Cache directory for response optimization
├── data/                # Data storage for processed news
├── newsfiles/          # Source news documents
└── ui/                  # User interface components
```

## Dependencies

- pathway[all]
- python-dotenv==1.0.1
- mpmath==1.3.0
- litellm>=1.35
- Google-generativeai
- Sentence-transformers

## How It Works

1. **News Input**: The system processes news articles from various sources
2. **Analysis**: Uses advanced NLP to analyze news content
3. **Verification**: Cross-references information with trusted sources
4. **Response Generation**: Provides accurate, verified information to user queries
5. **Source Tracking**: Maintains transparency by tracking and citing sources

## License

This project requires a valid Pathway license key to use advanced features.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, please open an issue in the repository. 
>>>>>>> other/main
