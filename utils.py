import os
from dotenv import load_dotenv
load_dotenv()

from pinecone import Pinecone
import google.generativeai as genai

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-flash-preview")


# -------------------------------
# PINECONE
# -------------------------------
def setup_pinecone():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    return pc.Index("mentor")


# -------------------------------
# ASK QUESTION (NO EMBEDDINGS)
# -------------------------------
def ask_question(query, index):

    # 🔥 Simple retrieval using query text (no embeddings)
    results = index.query(
        vector=[0]*1536,   # dummy vector (safe fallback)
        top_k=5,
        include_metadata=True
    )

    context = " ".join(
        [match["metadata"]["text"] for match in results["matches"]]
    )

    prompt = f"""
    You are a Data Structures expert.

    Answer clearly using the context.
    If not found, say "I don't know".

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "⚠️ API limit reached. Try later."