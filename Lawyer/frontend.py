import streamlit as st
import time
from rag_pipeline import answer_query, retrieve_docs, llm_model

# Custom CSS styling
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Arial', sans-serif !important;
    }

    h1, .stButton>button {
        font-family: 'Arial', sans-serif !important;
    }

    .chat-bubble {
        padding: 15px;
        border-radius: 10px;
        max-width: 80%;
        margin-bottom: 20px;
        font-size: 16px;
        line-height: 1.6;
    }

    .user-bubble {
        
        color: #999999;
        align-self: flex-end;
    }

    .thinking-label {
        color: #999999;
        font-size: 25px;
        font-style: italic;
        font-family: 'Arial', sans-serif !important;
        margin-bottom: 5px;
    }

    .ai-reasoning {
       
        color: #666666;
        font-family: 'Arial', sans-serif !important;
        font-size: 14px;
        line-height: 1.5;
    }

    .answer-label {
        font-weight: 400;
        color: #fffffff;
        font-size: 18px;
        font-family: 'Arial', sans-serif !important;
        margin-top: 20px;
    }

    .ai-answer {
        background-color: #ffffff;
        color: #000000;
        font-family: 'Gilroy', sans-serif !important;
        font-weight: 400;
        font-size: 20px;
        line-height: 1.8;
        border-left: 4px solid #000000;
        padding-left: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("AI Legal Assistant")

# PDF Upload
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

# Query Input
user_query = st.text_area("Enter your legal question:", height=150, placeholder="Ask about rights, laws, or legal scenarios.")

# Ask button
ask_question = st.button("Ask")

# If user submits query
if ask_question:
    if uploaded_file and user_query.strip() != "":
        # Show user's input
        st.markdown(f'<div class="chat-bubble user-bubble">{user_query}</div>', unsafe_allow_html=True)

        # Thinking animation
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown('<div class="thinking-label">Thinking...</div>', unsafe_allow_html=True)
        time.sleep(2)

        # Call RAG pipeline
        retrieved_docs = retrieve_docs(user_query)
        raw_response = answer_query(documents=retrieved_docs, model=llm_model, query=user_query)

        # Clear thinking
        thinking_placeholder.empty()
        time.sleep(0.5)

        # Handle response content
        if hasattr(raw_response, "content"):
            full_response = raw_response.content
        else:
            full_response = str(raw_response)

        # Split reasoning vs answer (based on "Answer:")
        if "Answer:" in full_response:
            reasoning_text = full_response.split("Answer:")[0].strip()
            final_answer = "Answer:" + full_response.split("Answer:")[-1].strip()
        else:
            reasoning_text = full_response
            final_answer = ""

        # Show reasoning in light gray with label
        if reasoning_text:
            st.markdown('<div class="thinking-label">AI is thinking...</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble ai-reasoning">{reasoning_text}</div>', unsafe_allow_html=True)

        # Show final answer bold & clear with label
        if final_answer:
            st.markdown('<div class="answer-label">Actual Answer</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble ai-answer">{final_answer}</div>', unsafe_allow_html=True)

    elif not uploaded_file:
        st.error("Please upload a valid PDF file.")
    else:
        st.warning("Please enter a legal question.")
