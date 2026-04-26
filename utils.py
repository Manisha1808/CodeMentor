import os
import time
from dotenv import load_dotenv

load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
import google.generativeai as genai

# Gemini setup (KEEPING YOUR MODEL)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3-flash-preview")


# -------------------------------
# RETRY FUNCTION (🔥 FIX)
# -------------------------------
def generate_with_retry(prompt):
    try:
        return model.generate_content(prompt).text
    except Exception as e:
        if "quota" in str(e).lower() or "429" in str(e):
            print("⚠️ Rate limit hit, retrying after 12s...")
            time.sleep(12)
            return model.generate_content(prompt).text
        return f"Error: {str(e)}"


# -------------------------------
# EMBEDDINGS
# -------------------------------
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )


# -------------------------------
# PINECONE
# -------------------------------
def setup_pinecone():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    return pc.Index("mentor")


# -------------------------------
# MAIN RAG FUNCTION
# -------------------------------
def ask_question(query, embeddings, index):

    # 🔥 FIX: remove extra API call (no fix_query)
    fixed_query = query.strip()

    enhanced_query = f"Explain data structures concept: {fixed_query}"
    query_vector = embeddings.embed_query(enhanced_query)

    results = index.query(
        vector=query_vector,
        top_k=6,
        include_metadata=True
    )

    context_chunks = []
    sources = []
    keyword = fixed_query.lower()

    for match in results["matches"]:
        text = match["metadata"]["text"]
        page = match["metadata"].get("page", "N/A")
        lower_text = text.lower()

        # remove junk
        if "appendix" in lower_text:
            continue

        # keep relevant
        if any(word in lower_text for word in keyword.split()):
            context_chunks.append(text)
            sources.append(f"Page {page}")

    # fallback
    if not context_chunks:
        for match in results["matches"]:
            context_chunks.append(match["metadata"]["text"])
            sources.append(f"Page {match['metadata'].get('page','N/A')}")

    # remove duplicates
    sources = list(set(sources))

    context = " ".join(context_chunks)

    prompt = f"""
    You are a Data Structures expert.

    Answer clearly using the context.
    If not found, say "I don't know".

    Context:
    {context}

    Question:
    {fixed_query}

    Answer:
    """

    # 🔥 FIX: use retry wrapper
    answer_text = generate_with_retry(prompt)

    return f"""
💡 Answer:
{answer_text}

📚 Sources:
{", ".join(sources)}
"""