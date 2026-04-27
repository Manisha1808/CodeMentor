import os
from dotenv import load_dotenv
load_dotenv()

from pinecone import Pinecone
import google.generativeai as genai

# Gemini setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-flash-preview")


DIMENSION = 384


# -------------------------------
# PINECONE
# -------------------------------
def setup_pinecone():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    return pc.Index("mentor")


# -------------------------------
# ASK QUESTION
# -------------------------------
def ask_question(query, index):
    try:
        results = index.query(
            vector=[0]*DIMENSION,
            top_k=5,
            include_metadata=True
        )

        context_chunks = []
        for match in results.get("matches", []):
            text = match.get("metadata", {}).get("text", "")
            if text:
                context_chunks.append(text)

        context = " ".join(context_chunks)

        prompt = f"""
You are a Data Structures expert.

First try to answer using the provided context.

If the context is weak or irrelevant, use your own knowledge to answer clearly and simply.

Context:
{context}

Question:
{query}

Answer:
"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print("ERROR:", e)
        return "⚠️ Something went wrong. Try again."