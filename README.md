🛡️ Anti-AI Uploader
Document Question Answering System (Django + DeepSeek API)

🔗 Live Demo:
👉 https://anti-ai-uploader.onrender.com/

The Anti-AI Uploader is a Django-based application that allows users to upload documents (PDF, DOCX, TXT, XLSX) and then ask questions about the content.
The system extracts text from the files, sends the text + question to the DeepSeek API, and generates context-aware answers.

This project demonstrates a clean, production-ready workflow for building AI-powered document intelligence using Python, Django, and DeepSeek.

🚀 Features
✔️ Multi-Document Upload

Supports:

PDF (pdfplumber)

DOCX (python-docx)

TXT

Excel (.xlsx) (openpyxl)

✔️ Automatic Text Extraction

Each file type is processed with the correct library:

PDF → pdfplumber

DOCX → python-docx

XLSX → openpyxl

TXT → decoded text

✔️ DeepSeek API Integration

The app sends your question + extracted document context to:

POST https://api.deepseek.com/v1/chat/completions


and retrieves the answer.

✔️ Clean Django UI

Simple upload page

Ask questions about uploaded content

Shows formatted AI responses

✔️ Production Ready

Runs on Render.com

Uses Gunicorn + WhiteNoise for serving static files

Environment variables (SECRET_KEY, API key) managed securely

Supports .env locally

🗂️ Project Structure
Anti AI Uploader/
│
├── anti_ai_uploader/        # Django project settings
├── uploader/                # App: views, utils, templates
│   ├── deepseek_utils.py    # API integration + text extraction
│   └── templates/
│
├── static/                  # CSS, JS files
├── templates/               # Base UI
│
├── requirements.txt
├── Procfile                 # For Render deployment
├── start.sh                 # Migration + Gunicorn startup
└── README.md

⚙️ Tech Stack
Component	Technology
Backend	Django 4.x
AI Model	DeepSeek API (deepseek-chat)
File Parsing	pdfplumber, python-docx, openpyxl
Server	Render Web Service
Static Files	WhiteNoise
Deployment	Gunicorn + Procfile
🔧 Installation (Local Development)
1️⃣ Clone the repo
git clone https://github.com/<your-username>/anti-ai-uploader.git
cd anti-ai-uploader

2️⃣ Create virtual env
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add environment variables

Create .env:

SECRET_KEY=your-secret-key
DEEPSEEK_API_KEY=your-api-key
DEBUG=True

5️⃣ Run locally
python manage.py runserver


Now open:
👉 http://127.0.0.1:8000/

🚀 Deploy on Render
Required environment variables:
SECRET_KEY=your-secret-key
DEEPSEEK_API_KEY=your-real-key
DEBUG=False
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1

Required files:

Procfile

web: bash ./start.sh


start.sh

#!/usr/bin/env bash
set -e
python manage.py migrate --noinput
exec gunicorn anti_ai_uploader.wsgi:application --bind 0.0.0.0:$PORT


Upload project → Render will auto build and deploy.

🧠 How the AI Response Works

User uploads file(s)

Text extracted from each file

User enters a question

App sends:

Context: <document text>
Question: <your question>


to DeepSeek API
5. Returns context-aware, accurate answers.



📌 Author

Madhesh SR

Email: madhesh704@gmail.com

