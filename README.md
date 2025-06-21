# AI Legal Reasoning Assistant

Hey! This is a little project I put together that uses AI to help you understand legal PDFs. You upload your legal document, ask questions about it, and the AI tries to give you clear answers and even explains how it got there.

It’s built around something called Retrieval-Augmented Generation, but don’t worry about that. Basically, it means the AI looks through your document carefully before answering.

---

## How to Get It Running

### What You’ll Need

Make sure you’ve got Python installed version 3.8 or higher. Also, you’ll need Ollama (it’s the thing that helps the AI understand text better) and a Groq API key (this is for the AI model).

### First Steps

Clone this repo to your machine:

```bash
git clone https://github.com/Hassan123j/AI-Reasoning-Chatbot.git
cd ai-legal-assistant
```

Then create a virtual environment and install everything:

```bash
python -m venv venv
source venv/bin/activate  # If you're on Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

If you don’t have the requirements file, here’s what you’ll want:

```
streamlit
langchain-groq
langchain-community
langchain-text-splitters
langchain-ollama
langchain-core
faiss-cpu  # or faiss-gpu if your machine can handle it
python-dotenv
```

### Setting Up Ollama

Download Ollama from their site and install it. Then grab the embedding model with:

```bash
ollama pull all-minilm
```

### Groq API Key

Sign up at Groq.com and get your API key. Then either put it in a `.env` file like this:

```
GROQ_API_KEY="your_api_key_here"
```

or export it in your terminal before you run the app:

```bash
export GROQ_API_KEY="your_api_key_here"
```

### Adding PDFs

Create a folder called `pdfs` and put your legal PDFs there. Like this:

```bash
mkdir pdfs
```

Throw in whatever PDFs you want to ask questions about.

### Build the Database

Run this once to get your PDFs ready for searching:

```bash
python vector_database.py
```

It’ll slice up the PDFs, make some smart vectors, and save them.

### Launch the App

Finally, start the app with:

```bash
streamlit run frontend.py
```

Your browser should pop up with the interface where you can upload docs, ask questions, and get answers.

---

## How To Use It

Just upload your PDF, type whatever you want to ask, and hit the Ask button. The AI will show you how it came up with the answer and then the answer itself.

---

## If You Wanna Tweak Stuff

Feel free to swap the AI model or embedding model if you want. You can also change how the PDFs get sliced or how the AI responds by editing some files no pressure, it’s all in the code.

---

## File Rundown

* `frontend.py` — the UI you interact with
* `rag_pipeline.py` — this is the AI brain that figures out answers
* `vector_database.py` — turns your PDFs into searchable bits
* `pdfs/` — drop your PDFs here
* `vectorstore/` — where all the data is saved after processing

---

## Help Wanted

If you see ways to improve, just jump in! Fork, raise issues, or send a pull request. I’m happy to collaborate.
