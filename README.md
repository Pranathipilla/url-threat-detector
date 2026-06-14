## URL Threat Detector

URL Threat Detector is a cybersecurity tool that uses Machine Learning and 
Natural Language Processing to detect malicious URLs in real time.

Most phishing attacks, malware, and scams start with a suspicious link. 
This tool helps users identify threats before clicking.

### How it works

URLs are text — but ML models need numbers. So the pipeline works like this:

1. **NLP (TF-IDF)** converts the URL text into numerical vectors by analyzing 
   character and word patterns. Words like "login", "verify", "free", "bank" 
   appearing in suspicious combinations get weighted higher.

2. **Random Forest** (an ensemble ML model) takes those vectors and classifies 
   the URL as malicious or benign based on patterns learned from 450,000 
   real-world URLs.

3. **orca-mini LLM** (via Ollama) then explains the prediction in plain English — 
   why the URL looks suspicious and what the user should do.

4. **BeautifulSoup** allows scanning an entire webpage — it extracts all links 
   from any page and runs each one through the ML model automatically, 
   generating a full threat report.

The model achieves 99% accuracy on the test set with balanced class sampling 
to handle the natural imbalance between malicious and benign URLs in the wild.
## Features
- Detects malicious vs benign URLs using Random Forest + TF-IDF (NLP)
- LLM-powered explanation of why a URL is flagged (orca-mini via Ollama)
- Scan entire webpages and check all links at once (BeautifulSoup)
- Clean web UI built with Flask

## Tech Stack
Python · Flask · scikit-learn · TF-IDF · Random Forest · BeautifulSoup · orca-mini

## Dataset
Download dataset from Kaggle: https://www.kaggle.com/datasets/siddharthkumar25/malicious-and-benign-urls

Place as `urldata.csv` in root folder before running.

## Run locally
pip install flask flask-cors scikit-learn beautifulsoup4 requests ollama
python app.py
