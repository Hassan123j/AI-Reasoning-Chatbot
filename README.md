# AI Legal Assistant

This project implements an AI Legal Assistant using a Retrieval-Augmented Generation (RAG) pipeline. It allows users to upload PDF legal documents, ask questions based on the content of those documents, and receive answers along with the AI's reasoning.

## Features

* **PDF Upload:** Upload your legal documents in PDF format.
* **Question Answering:** Ask specific questions related to the content of the uploaded PDF.
* **RAG Pipeline:** Leverages a RAG architecture for more accurate and context-aware responses.
    * **Document Loading & Chunking:** Processes PDF documents, splitting them into manageable chunks.
    * **Vector Database:** Stores document embeddings in a FAISS vector store for efficient similarity search.
    * **LLM Integration:** Uses the DeepSeek R1 Distill model via the Groq API for generating answers.
* **Clear UI:** A user-friendly interface built with Streamlit, providing real-time feedback and distinct sections for AI reasoning and the final answer.
* **Custom Styling:** Enhanced visual appeal with custom CSS for chat bubbles and text elements.

## Architecture Overview

The system consists of three main components:

1.  **`frontend.py` (Streamlit Application):** Handles the user interface, PDF uploads, query input, and displays the AI's responses. It interacts with the `rag_pipeline` to get answers.
2.  **`rag_pipeline.py` (RAG Logic):** Orchestrates the core RAG process. It defines how documents are retrieved from the vector database and how the Language Model (LLM) is prompted to generate answers based on the retrieved context. It uses the `ChatGroq` model.
3.  **`vector_database.py` (Document Processing & Storage):** Responsible for loading PDF documents, splitting them into chunks, generating embeddings using `OllamaEmbeddings` (with `all-minilm` model), and storing these embeddings in a FAISS vector database.

## Setup and Installation

Follow these steps to set up and run the AI Legal Assistant on your local machine.

### Prerequisites

* Python 3.8+
* Pip (Python package installer)
* Ollama (for local embedding model)

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd ai-legal-assistant
```

### 2. Install Dependencies

It's recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
pip install -r requirements.txt
```

**Note:** A `requirements.txt` file is assumed to exist with the necessary libraries. If not, you will need to create one with the following content:

```
streamlit
langchain-groq
langchain-community
langchain-text-splitters
langchain-ollama
langchain-core
faiss-cpu # or faiss-gpu if you have a compatible GPU
python-dotenv # if you use .env for API key
```

### 3. Set up Ollama for Embeddings

The `vector_database.py` uses Ollama to run the `all-minilm` embedding model locally.

* **Download and Install Ollama:** Follow the instructions on the [Ollama website](https://ollama.com/download) to install Ollama for your operating system.
* **Pull the `all-minilm` model:** Once Ollama is installed, open your terminal and run:
    ```bash
    ollama pull all-minilm
    ```

### 4. Configure Groq API Key

The `rag_pipeline.py` uses the Groq API for the LLM.

* **Get a Groq API Key:** Sign up on the [Groq website](https://groq.com/) to obtain your API key.
* **Set as Environment Variable:**
    * **Recommended:** Create a `.env` file in the root directory of your project and add your API key:
        ```
        GROQ_API_KEY="your_groq_api_key_here"
        ```
        Ensure `python-dotenv` is installed (`pip install python-dotenv`), and `load_dotenv()` is uncommented in `rag_pipeline.py` if you choose this method.
    * **Alternatively (less secure for production):** Set it directly in your shell before running the app:
        ```bash
        export GROQ_API_KEY="your_groq_api_key_here" # For Linux/macOS
        # set GROQ_API_KEY="your_groq_api_key_here" # For Windows CMD
        # $env:GROQ_API_KEY="your_groq_api_key_here" # For Windows PowerShell
        ```

### 5. Place Your PDF Documents

The `vector_database.py` expects a `pdfs/` directory to exist.
* Create a `pdfs` folder in your project's root directory:
    ```bash
    mkdir pdfs
    ```
* Place the `universal_declaration_of_human_rights.pdf` file (or any other PDF you want to use initially) inside this `pdfs/` directory.

### 6. Initialize the Vector Database

The `vector_database.py` script needs to be run *once* to process the initial PDF and create the FAISS vector store.

```bash
python vector_database.py
```
This will create a `vectorstore/db_faiss` directory containing your vector database.

### 7. Run the Streamlit Application

```bash
streamlit run frontend.py
```

This will open the Streamlit application in your web browser, usually at `http://localhost:8501`.

## Usage

1.  **Upload PDF:** Click the "Upload a PDF document" button and select your PDF file.
2.  **Enter Question:** Type your legal question into the text area.
3.  **Ask:** Click the "Ask" button.
4.  **View Response:** The AI's reasoning will appear first, followed by the "Actual Answer."

## Customization

* **LLM Model:** You can change the `model` parameter in `rag_pipeline.py` to use other Groq-supported models.
* **Embedding Model:** In `vector_database.py`, modify `ollama_model_name` to use a different local Ollama embedding model. Remember to `ollama pull` the new model.
* **Chunking Strategy:** Adjust `chunk_size` and `chunk_overlap` in `vector_database.py` to optimize document splitting for your specific use case.
* **Prompt Template:** Modify `custom_prompt_template` in `rag_pipeline.py` to guide the LLM's response style and constraints.
* **UI/CSS:** Customize the CSS in `frontend.py` to change the appearance of the chat interface.

## Project Structure

```
.
├── frontend.py
├── rag_pipeline.py
├── vector_database.py
├── pdfs/
│   └── universal_declaration_of_human_rights.pdf # Example PDF
├── vectorstore/
│   └── db_faiss/ # FAISS vector database files (generated)
├── .env                  # For storing API keys (optional, but recommended)
└── requirements.txt      # Python dependencies
```

## Contributing

Feel free to fork this repository, submit pull requests, or open issues to improve the project.
