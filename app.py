import logging
import sys
import click
import pathway as pw
import yaml
import os
from dotenv import load_dotenv
from pathway.udfs import DiskCache
from pathway.xpacks.llm.question_answering import BaseRAGQuestionAnswerer
from pathway.stdlib.indexing import BruteForceKnnFactory
from pathway.xpacks.llm import embedders, llms, parsers, splitters
from pathway.xpacks.llm.document_store import DocumentStore
from pathway.stdlib.indexing import TantivyBM25Factory, HybridIndexFactory

# Load environment variables (e.g., API keys) from the .env file.
load_dotenv()

# Set your Pathway license key here to use advanced features.
pw.set_license_key(os.environ.get("LICENCE_KEY", "PATHWAY-KEY-NOT-FOUND"))

# Set up basic logging to capture key events and errors.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# Command-line interface (CLI) function to run the app with a specified config file.
@click.command()
@click.option("--config_file", default="app.yaml", help="Config file to be used.")
def run(config_file: str = "app.yaml"):
    # Load the configuration from the YAML file.
    with open(config_file) as f:
        config = pw.load_yaml(f)

    sources = config["sources"]

    llm = llms.LiteLLMChat(model="gemini/gemini-2.5-pro-exp-03-25", cache_strategy=DiskCache())

    parser = parsers.UnstructuredParser()

    text_splitter = splitters.TokenCountSplitter(max_tokens=400)

    embedding_model = "avsolatorio/GIST-small-Embedding-v0"

    embedder = embedders.SentenceTransformerEmbedder(
        embedding_model,
        call_kwargs={"show_progress_bar": False}
    )

    index = BruteForceKnnFactory(embedder=embedder)
    
    # ✅ Set up Hybrid Index (BM25 + FAISS)
    bm25_index = TantivyBM25Factory()  # Keyword-based text search
    # faiss_index = FaissIndexFactory(embedder=embedder)  # Vector-based semantic search
    hybrid_index = HybridIndexFactory([bm25_index, index])  # Combine both


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
            retriever_factory=hybrid_index
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
