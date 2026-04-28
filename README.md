# ⚡ Code Mentor AI (RAG Powered)

An AI-powered **Data Structures & Algorithms Mentor** that helps users understand concepts using **retrieval-augmented generation (RAG)** with real contextual knowledge.

---

## 🌐 Live Demo

* 🔗 Previous Version (Flask + Gemini):
  https://code-mentor-smy0.onrender.com/

* 🔗 Latest Version (RAG + Hugging Face):
  https://huggingface.co/spaces/Manisha1808/CodeMentor

---

## 🚀 What’s New (Major Upgrade)

This version is **not just a chatbot anymore**.

### ✅ RAG-Based Architecture

* Uses **vector search (Pinecone)** to fetch relevant DSA content
* Ensures **accurate + context-grounded answers**

### 🧠 Context-Aware Responses

* Answers are generated ONLY from retrieved knowledge
* Avoids hallucination

### ⚡ Faster & Smarter Retrieval

* Embeddings via `all-MiniLM-L6-v2`
* Top-k semantic search for best matches

### 🎯 Controlled AI Behavior

* If answer not found → returns *“I don't know”*
* Prevents incorrect explanations

---

## 🔥 Features

### 🧠 DSA Mentor Mode

* Answers strictly related to Data Structures & Algorithms
* Beginner-friendly explanations
* Context-backed answers

### 🔍 Semantic Search (Pinecone)

* Retrieves most relevant chunks from knowledge base
* Improves answer quality

### 🤖 AI Generation (Gemini)

* Uses Google Gemini for final response generation

### 💬 Interactive Chat UI

* Built using Gradio
* Clean dark theme interface

---

## 🛠️ Tech Stack

| Layer      | Technology            |
| ---------- | --------------------- |
| Frontend   | Gradio                |
| Backend    | Python                |
| Embeddings | Sentence Transformers |
| Vector DB  | Pinecone              |
| LLM        | Google Gemini         |
| Deployment | Hugging Face Spaces   |

---

## 📂 Project Structure

```
CodeMentor/
│
├── app.py
├── ingest.py
├── requirements.tx
```

---

## ⚙️ How It Works (Architecture)

1. User enters a question
2. Question → converted into embedding
3. Query sent to Pinecone
4. Top relevant context retrieved
5. Context + question → sent to Gemini
6. Final answer returned to user

---

## 🔐 Environment Variables

Add these before running:

```
PINECONE_API_KEY=your_key
GEMINI_API_KEY=your_key
```

---

## ⚙️ Installation (Local Setup)

```bash
git clone https://github.com/your-username/code-mentor-ai.git
cd code-mentor-ai

pip install -r requirements.txt
```

Run:

```bash
python app.py
```

---
## Output

### Flask(Version)

<img width="975" height="465" alt="image" src="https://github.com/user-attachments/assets/84dc292b-51af-41a4-9e6e-077da6543766" />

<img width="975" height="464" alt="image" src="https://github.com/user-attachments/assets/250feaa5-7894-4401-92e2-47819e6598e1" />

<img width="975" height="468" alt="image" src="https://github.com/user-attachments/assets/36a64263-6514-419f-8fec-9a60e52d5247" />

<img width="975" height="464" alt="image" src="https://github.com/user-attachments/assets/aeb71d66-4b47-4d5d-9fd0-0fff424eb56e" />

### Gradio(Version)

<img width="1192" height="634" alt="image" src="https://github.com/user-attachments/assets/edd70c82-86d3-4a60-9cb2-b20136a19d3a" />

---

## ⚠️ Limitations

* Gemini API rate limits (free tier)
* Initial load may be slow due to model download

---

## 💡 Future Improvements

* Better UI (custom frontend instead of Gradio)
* Chat history persistence
* Multi-topic knowledge base
* Offline LLM fallback (no API dependency)

---

## 🙌 Acknowledgements

* Google Gemini API
* Pinecone Vector Database
* Hugging Face Spaces
* Sentence Transformers

---

## 👩‍💻 Author

**Manisha Sen**

---

## ⭐ Key Highlight (For Recruiters)

> Built a **RAG-based AI system** using vector databases and LLMs to deliver context-aware DSA explanations, reducing hallucinations and improving answer accuracy.
