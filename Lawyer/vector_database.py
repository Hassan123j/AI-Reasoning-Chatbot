# Imports
from langchain_community.document_loaders import PDFPlumberLoader         # For loading PDF files
from langchain_text_splitters import RecursiveCharacterTextSplitter       # For splitting documents into smaller chunks
from langchain_ollama import OllamaEmbeddings                             # For generating embeddings using local Ollama models
from langchain_community.vectorstores import FAISS                        # FAISS vector store for fast similarity search

# Directory to store uploaded PDFs
pdfs_directory = 'pdfs/'

# Step 1: PDF Upload and Loading

def upload_pdf(file):
    """
    Uploads a PDF file to the specified directory.

    Args:
        file (UploadedFile): File-like object (e.g., from Streamlit).
    """
    with open(pdfs_directory + file.name, "wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    """
    Loads a PDF file using PDFPlumberLoader.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        List[Document]: Parsed pages from the PDF as LangChain Document objects.
    """
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    return documents

# Load a specific PDF file (can be changed dynamically)
file_path = 'universal_declaration_of_human_rights.pdf'
documents = load_pdf(file_path)
# print("PDF pages: ", len(documents))

# Step 2: Split Text into Chunks

def create_chunks(documents): 
    """
    Splits documents into smaller chunks for efficient processing and embedding.

    Args:
        documents (List[Document]): Raw documents to be chunked.

    Returns:
        List[Document]: Chunks of the original documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,           # Max characters per chunk
        chunk_overlap=200,         # Overlap to maintain context
        add_start_index=True       # Track where each chunk begins
    )
    text_chunks = text_splitter.split_documents(documents)
    return text_chunks

text_chunks = create_chunks(documents)
# print("Chunks count: ", len(text_chunks))

# Step 3: Initialize Embedding Model (via Ollama)

ollama_model_name = "all-minilm"  # Lightweight, fast local model

def get_embedding_model(model_name):
    """
    Returns the embedding model using Ollama.

    Args:
        model_name (str): Name of the local Ollama embedding model.

    Returns:
        OllamaEmbeddings: Embedding model object.
    """
    embeddings = OllamaEmbeddings(model=model_name)
    return embeddings

# Step 4: Store Embeddings in FAISS Vector Store

FAISS_DB_PATH = "vectorstore/db_faiss"  # Directory to save FAISS DB

# Create vector store from chunks using the embedding model
faiss_db = FAISS.from_documents(text_chunks, get_embedding_model(ollama_model_name))

# Save the vector database locally for reuse
faiss_db.save_local(FAISS_DB_PATH)
