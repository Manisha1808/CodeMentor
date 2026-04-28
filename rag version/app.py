import os
import gradio as gr
from dotenv import load_dotenv
load_dotenv()

from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from google import genai

# -------------------------------
# SETUP
# -------------------------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("mentor")

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# -------------------------------
# RAG FUNCTION
# -------------------------------
def ask_question(query, history):
    try:
        # Embed query
        query_vector = embed_model.encode(query).tolist()

        # Search Pinecone
        results = index.query(
            vector=query_vector,
            top_k=5,
            include_metadata=True
        )

        # Build context
        context_chunks = [
            m.get("metadata", {}).get("text", "")
            for m in results.get("matches", [])
            if m.get("metadata", {}).get("text", "")
        ]

        if not context_chunks:
            answer = "⚠️ No relevant context found."
        else:
            context = " ".join(context_chunks)

            prompt = f"""
You are a Data Structures expert.

Answer ONLY using the context below.
If answer not found, say "I don't know".

Context:
{context}

Question:
{query}
"""

            try:
                res = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt
                )
                answer = res.text
            except:
                answer = "⚠️ Gemini API limit reached."

        # ✅ ONLY DICT FORMAT (NO TUPLES ANYWHERE)
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": answer})

        return history, ""

    except Exception as e:
        print("ERROR:", e)

        history.append({
            "role": "assistant",
            "content": "⚠️ Something went wrong"
        })

        return history, ""


# -------------------------------
# UI
with gr.Blocks(
    theme=gr.themes.Soft(
        primary_hue="indigo",
        secondary_hue="violet",
        neutral_hue="slate"
    ),
    css="""
/* ===== FORCE DARK ROOT ===== */
:root, body, .gradio-container {
    background: #0f172a !important;
    color: #e5e7eb !important;
}

/* REMOVE LIGHT CARDS */
.gradio-container > div {
    background: transparent !important;
}

/* ===== CHATBOX ===== */
.gr-chatbot {
    background: #1e293b !important;
    border-radius: 14px !important;
    border: 1px solid #334155 !important;
}

/* FIX INNER WHITE */
.gr-chatbot .wrap {
    background: transparent !important;
}

/* ===== MESSAGE ===== */
.gr-chatbot .message {
    background: #334155 !important;
    color: #f1f5f9 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
}

/* USER MESSAGE */
.gr-chatbot .message.user {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
}

/* ===== INPUT ===== */
textarea {
    background: #020617 !important;
    color: white !important;
    border-radius: 999px !important;
    border: 1px solid #475569 !important;
}

/* ===== BUTTON ===== */
button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border-radius: 999px !important;
}

/* TEXT */
h1 { color: #c4b5fd !important; }
p { color: #94a3b8 !important; }

/* REMOVE FOOTER */
footer { display: none !important; }
"""
) as demo:

    with gr.Column(elem_classes="main"):

        gr.Markdown(
            "<h1 style='text-align:center; color:#a78bfa;'>⚡ Code Mentor</h1>"
        )
        gr.Markdown(
            "<p style='text-align:center; color:#94a3b8;'>Your Personal DSA Instructor</p>"
        )

        chatbot = gr.Chatbot(height=500)
        state = gr.State([])

        with gr.Row():
            txt = gr.Textbox(
                placeholder="Ask something...",
                show_label=False,
                scale=8
            )
            btn = gr.Button(" Send", scale=1)

        btn.click(ask_question, [txt, state], [chatbot, txt])
        txt.submit(ask_question, [txt, state], [chatbot, txt])


if __name__ == "__main__":
    demo.launch()
