from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

from utils import get_embeddings, setup_pinecone, ask_question

load_dotenv()

app = Flask(__name__)

embeddings = get_embeddings()
index = setup_pinecone()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    query = request.form["query"]
    answer = ask_question(query, embeddings, index)
    return answer


if __name__ == "__main__":
    app.run(debug=True)