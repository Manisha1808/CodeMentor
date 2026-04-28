from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types
import os

app = Flask(__name__)


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """
You are a strict Data Structures and Algorithms instructor.

Rules:
1. Only answer DSA-related questions
2. Explain in simple and beginner-friendly way
3. Use examples when needed

If question is NOT related to DSA:
Reply ONLY:
"Ask me something related to Data Structures and Algorithms."
"""

@app.route("/")
def home():
    return render_template("index.html")  # connect frontend

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_input = data.get("question", "").strip()

        if not user_input:
            return jsonify({"answer": "Please enter a question."})

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            ),
            contents=user_input
        )

        return jsonify({"answer": response.text})

    except Exception as e:
        return jsonify({"answer": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
