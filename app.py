from flask import Flask, render_template, request
import os
from dotenv import load_dotenv

from utils import setup_pinecone, ask_question

load_dotenv()

app = Flask(__name__)

# Setup
index = setup_pinecone()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    query = request.form["query"]
    answer = ask_question(query, index)
    return answer


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)