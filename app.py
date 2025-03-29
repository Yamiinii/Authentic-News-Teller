import logging
import sys
import click
import pathway as pw
import yaml
from dotenv import load_dotenv
from pathway.udfs import DiskCache
from pathway.xpacks.llm.question_answering import BaseRAGQuestionAnswerer
from pathway.stdlib.indexing import BruteForceKnnFactory
from pathway.xpacks.llm import embedders, llms, parsers, splitters
from pathway.xpacks.llm.document_store import DocumentStore

# Set your Pathway license key here to use advanced features.
pw.set_license_key("demo-license-key-with-telemetry")

# Set up basic logging to capture key events and errors.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Load environment variables (e.g., API keys) from the .env file.
load_dotenv()

import pandas as pd

def load_news_data(file_path="all_news.xlsx"):
    try:
        news_data = pd.read_excel(file_path)
        if news_data.empty:
            return pd.DataFrame()
        
        # Combine relevant text fields for better retrieval
        news_data["text"] = news_data.apply(
            lambda row: f"Title: {row['Title']}\n"
                        f"Author: {row['Author']}\n"
                        f"Source: {row['Source']}\n"
                        f"Published At: {row['Published At']}\n"
                        f"Description: {row['Description']}\n"
                        f"Content: {row['Content']}\n"
                        f"URL: {row['URL']}",
            axis=1
        )

        return news_data
    except Exception as e:
        logging.error(f"Error loading news data: {e}")
        return pd.DataFrame()


# Command-line interface (CLI) function to run the app with a specified config file.
@click.command()
@click.option("--config_file", default="app.yaml", help="Config file to be used.")
def run(config_file: str = "app.yaml"):
    # Load the configuration from the YAML file.
    with open(config_file) as f:
        config = pw.load_yaml(f)

    news_data = load_news_data()
    
    if news_data.empty:
        logging.warning("No news data found. The RAG system may not function correctly.")
    
    # Convert articles into a Pathway source
    sources = list(news_data["text"])

    llm = llms.LiteLLMChat(model="gemini/gemini-2.5-pro-exp-03-25", cache_strategy=DiskCache())

    parser = parsers.UnstructuredParser()

    text_splitter = splitters.TokenCountSplitter(max_tokens=400)

    embedding_model = "avsolatorio/GIST-small-Embedding-v0"

    embedder = embedders.SentenceTransformerEmbedder(
        embedding_model,
        call_kwargs={"show_progress_bar": False}
    )

    index = BruteForceKnnFactory(embedder=embedder)

    # Host and port configuration for running the server.
    pathway_host: str = "0.0.0.0"
    pathway_port: int = 8000

    # Initialize the vector store for storing document embeddings in memory.
    # This vector store updates the index dynamically whenever the data source changes
    # and can scale to handle over a million documents.
    doc_store = DocumentStore(
            docs=sources,
            splitter=text_splitter,
            parser=parser,
            retriever_factory=index
        )

    # Create a RAG (Retrieve and Generate) question-answering application.
    rag_app = BaseRAGQuestionAnswerer(llm=llm, indexer=doc_store)

    # Build the server to handle requests at the specified host and port.
    rag_app.build_server(host=pathway_host, port=pathway_port)

    # Run the server with caching enabled, and handle errors without shutting down.
    rag_app.run_server(with_cache=True, terminate_on_error=False)

# Entry point to execute the app if the script is run directly.
if __name__ == "__main__":
    run()
