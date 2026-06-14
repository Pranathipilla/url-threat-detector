from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests as req
import pickle
import threading

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

print("Model loaded and ready!")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data["url"]
    X = vectorizer.transform([url])
    prediction = model.predict(X)[0]
    confidence = model.predict_proba(X)[0].max()
    return jsonify({
        "url": url,
        "prediction": "malicious" if prediction == 1 else "benign",
        "confidence": round(float(confidence) * 100, 2)
    })

@app.route("/scan", methods=["POST"])  # ← was missing this
def scan():
    data = request.get_json()
    page_url = data["url"]
    try:
        response = req.get(page_url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("http"):
                links.append(href)
        results = []
        for link in links[:20]:
            X = vectorizer.transform([link])
            prediction = model.predict(X)[0]
            confidence = model.predict_proba(X)[0].max()
            results.append({
                "url": link,
                "prediction": "malicious" if prediction == 1 else "benign",
                "confidence": round(float(confidence) * 100, 2)
            })
        malicious = [r for r in results if r["prediction"] == "malicious"]
        benign = [r for r in results if r["prediction"] == "benign"]
        return jsonify({
            "page": page_url,
            "total": len(results),
            "malicious_count": len(malicious),
            "benign_count": len(benign),
            "results": results
        })
    except Exception as e:
        print(f"Scan error:{e}")
        return jsonify({
            "page":page_url,
            "total":0,
            "malicious_count":0,
            "benign_count":0,
            "results":[],
            "error": str(e)}), 200
    

if __name__ == "__main__":
    app.run(debug=False, port=5000)