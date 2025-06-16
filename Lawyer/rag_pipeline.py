# Import necessary libraries
from langchain_groq import ChatGroq                    # LLM interface for Groq API
from vector_database import faiss_db                  # FAISS vector DB for document retrieval
from langchain_core.prompts import ChatPromptTemplate # For formatting the chat prompt
import os                                             # To access environment variables

# Optional: Uncomment and use if you're not using pipenv or another env manager
# from dotenv import load_dotenv
# load_dotenv()

# Step 1: Setup LLM (Language Model)
# Initialize the LLM with DeepSeek R1 Distill model using Groq API
# API key is retrieved securely from environment variables
llm_model = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    api_key=os.getenv("GROQ_API_KEY")
)

# Step 2: Document Retrieval

def retrieve_docs(query):
    """
    Retrieves documents relevant to the input query using FAISS vector search.
    
    Args:
        query (str): The user query or question.
        
    Returns:
        List[Document]: A list of documents similar to the query.
    """
    return faiss_db.similarity_search(query)

def get_context(documents):
    """
    Concatenates the content of retrieved documents to form a single context string.
    
    Args:
        documents (List[Document]): List of documents retrieved from FAISS.
        
    Returns:
        str: Combined text content of all documents separated by double newlines.
    """
    context = "\n\n".join([doc.page_content for doc in documents])
    return context

# Step 3: Define Custom Prompt Template

# Template for prompting the model with a question and supporting context
custom_prompt_template = """
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer. 
Dont provide anything out of the given context

Question: {question} 
Context: {context} 
Answer:
"""

def answer_query(documents, model, query):
    """
    Uses the LLM to answer a query based on retrieved documents and a custom prompt.
    
    Args:
        documents (List[Document]): Relevant documents retrieved via FAISS.
        model (ChatGroq): The initialized Groq LLM model.
        query (str): The question posed by the user.
        
    Returns:
        str: The model's response to the question.
    """
    # Prepare context from documents
    context = get_context(documents)
    
    # Build prompt using the defined template
    prompt = ChatPromptTemplate.from_template(custom_prompt_template)
    
    # Create a chain (pipeline) that formats the prompt and passes it to the model
    chain = prompt | model
    
    # Invoke the chain with the actual input
    return chain.invoke({"question": query, "context": context})
