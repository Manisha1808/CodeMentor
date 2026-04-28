import time
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv()

# -------------------------------
# PINECONE SETUP
# -------------------------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("mentor")   # ⚠️ your existing index (384)

# -------------------------------
# EMBEDDING MODEL (HF)
# -------------------------------
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------------
# LOAD PDF
# -------------------------------
loader = PyPDFLoader("document/dsa.pdf")
docs = loader.load()

# -------------------------------
# CHUNKING
# -------------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(docs)

# -------------------------------
# UPSERT TO PINECONE
# -------------------------------
vectors = []

print("🚀 Generating embeddings...")

for i, chunk in enumerate(chunks):
    try:
        text = chunk.page_content
        embedding = embed_model.encode(text).tolist()

        vectors.append({
            "id": str(i),
            "values": embedding,
            "metadata": {
                "text": text,
                "page": chunk.metadata.get("page", "N/A")
            }
        })

        # batch upload
        if len(vectors) == 20:
            index.upsert(vectors)
            vectors = []
            print(f"✅ Uploaded batch {i}")

        time.sleep(0.2)

    except Exception as e:
        print(f"⚠️ Skipped chunk {i}: {e}")

# upload remaining
if vectors:
    index.upsert(vectors)

print("✅ Data uploaded successfully!")
