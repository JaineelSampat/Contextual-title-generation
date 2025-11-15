Multimodal AI-Driven Contextual Story Title Generator

A BLIP-based Web Application for Generating Contextual Titles with BERTScore Evaluation

📘 Overview

This project is a multimodal AI web application that generates meaningful, context-aware titles from a story + image pair using the BLIP (Bootstrapped Language Image Pretraining) model.
It evaluates the generated title using BERTScore, ensuring strong semantic alignment (≥ 0.85).

The system includes:

Frontend: React + Vite

Backend: Python, Flask, Hugging Face Transformers

Model: BLIP (Salesforce/blip-image-captioning-base)

Metric: BERTScore (evaluate library)

✨ Features

Accepts story text + image as input

Generates a contextual, concise title using BLIP

Computes BERTScore (F1) based on reference title

Frontend–backend communication via REST API

Clean UI for file uploads, text entry, and results display

🧠 How It Works

User uploads an image and story text.

Backend extracts key semantic elements and feeds them with the image to BLIP.

BLIP generates a contextual, title-like caption.

BERTScore compares generated title with the reference title.

Result is displayed in the frontend.

📂 Project Structure
miltimodalblipdemo/
│
├── backend/
│   ├── app.py              # Flask API
│   ├── model_utils.py      # BLIP title generation + BERTScore logic
│   ├── requirements.txt
│   └── .venv/              # Python virtual environment
│
└── frontend/
    ├── src/
    │   ├── App.jsx         # UI logic
    │   ├── components/     # Form + UI components
    │   └── styles/
    ├── package.json
    └── vite.config.js

🚀 Getting Started
Backend Setup
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py


Backend runs at:
http://127.0.0.1:8000

Frontend Setup
cd frontend
npm install
npm run dev


Frontend runs at:
http://localhost:5173

📝 API Endpoint
POST /generate_title

Request body:

{
  "story_text": "string",
  "image_base64": "base64 string",
  "reference_title": "string"
}


Response:

{
  "generated_title": "string",
  "bertscore": 0.88
}

🔧 Requirements

Python 3.9+

Node.js 20.19+

HuggingFace Transformers

Flask

React + Vite

Full list in requirements.txt and package.json.

📜 License

MIT License.

🙌 Acknowledgements

Salesforce Research — BLIP

HuggingFace Transformers

Google Research — BERTScore metric
