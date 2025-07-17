from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = "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"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json.get("message", "").strip()

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "CreatorsBot"
    }

    payload = {
        "model": "openrouter/auto",
        "max_tokens": 300,
        "messages": [
            {"role": "system", "content": "You are a Creators Bot that teaches content creation in Hinglish. Always reply with useful, fun, step-by-step instructions for beginners."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        if res.status_code == 200:
            reply = res.json()["choices"][0]["message"]["content"]
            return jsonify({"response": reply})
        else:
            return jsonify({"response": f"⚠️ API error: {res.text}"})
    except Exception as e:
        return jsonify({"response": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
