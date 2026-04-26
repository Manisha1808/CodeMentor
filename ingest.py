from utils import get_embeddings, setup_pinecone
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# -------------------------------
# LOAD DOCUMENT
# -------------------------------
def load_document(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()


# -------------------------------
# CHUNKING
# -------------------------------
def chunk_data(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(documents)


# -------------------------------
# STORE VECTORS (UPDATED)
# -------------------------------
def store_vectors(chunks, embeddings, index):

    vectors = []

    for i, chunk in enumerate(chunks):
        vector = embeddings.embed_query(chunk.page_content)

        vectors.append({
            "id": str(i),
            "values": vector,
            "metadata": {
                "text": chunk.page_content,
                "page": chunk.metadata.get("page", "N/A")   # 🔥 IMPORTANT
            }
        })

    index.upsert(vectors)
    print(f"✅ Stored {len(vectors)} vectors")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":

    embeddings = get_embeddings()
    index = setup_pinecone()

    docs = load_document("document/dsa.pdf")
    chunks = chunk_data(docs)

    # clear old data (IMPORTANT)
    index.delete(delete_all=True)

    store_vectors(chunks, embeddings, index)