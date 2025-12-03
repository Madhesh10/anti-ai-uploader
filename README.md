
# 🛡️ Anti-AI Uploader  
### Document Question-Answering System (Django + DeepSeek API)

Anti-AI Uploader is a **Document Intelligence Web Application** built using  
**Python, Django, DeepSeek API, and Render hosting**.  
Users can upload documents and ask questions, and the system intelligently answers based only on the document’s content.

This project acts like a **personal AI analyst** — useful for resumes, reports, academic papers, legal documents, corporate files, and more.

---

## 🚀 Features

### 📄 **1. Multi-File Upload System**
Supports:
- PDF  
- DOCX  
- TXT  
- Excel (XLSX)  
- Other text-based files  

### 🔍 **2. Automatic Text Extraction**
Uses:
- `pdfplumber` — PDF parsing  
- `python-docx` — DOCX reading  
- `openpyxl` — Excel sheet extraction  
- Built-in fallback for plain text files  

### 🤖 **3. DeepSeek AI Question Answering**
The app sends extracted text + user query to DeepSeek:

- Fast API responses  
- No OpenAI dependency  
- Only answers using document context  

### 🌐 **4. Django Backend**
- Django views for upload & processing  
- Secure file handling  
- Clean, maintainable code structure  

### ☁️ **5. Render Deployment Support**
This project includes:
- `requirements.txt` ready for deployment  
- `Procfile` + `start.sh` for migrations  
- Environment variable–based configuration  
- Static file support via WhiteNoise  

Works on the **free Render tier**.

---

## 🗂️ Project Structure

```

Anti-AI-Uploader/
│── anti_ai_uploader/      # Django project settings
│── uploader/              # Main application logic
│   ├── views.py
│   ├── deepseek_utils.py  # API integration & text extraction
│   ├── templates/
│── static/
│── templates/
│── requirements.txt
│── Procfile
│── start.sh

```

---

## 🔑 Environment Variables (Render / Local)

Create a `.env` file or set in Render dashboard:

```

SECRET_KEY=your-django-secret-key
DEBUG=False
DEEPSEEK_API_KEY=your-deepseek-api-key
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1

```

---

## 🧠 How It Works

### 1️⃣ Upload a document  
User uploads any supported file.

### 2️⃣ Text is extracted  
Using the correct parser depending on file type.

### 3️⃣ User asks a question  
The system prepares:

```

Context: <extracted-text>

Question: <user-question>

````

### 4️⃣ DeepSeek API responds  
Your AI assistant answers only using document content.

---

## ▶️ Local Development

### Install dependencies:
```bash
pip install -r requirements.txt
````

### Run the server:

```bash
python manage.py runserver
```

---

## ☁️ Deployment on Render

### 1️⃣ Push project to GitHub

Render pulls from your repository.

### 2️⃣ Add environment variables

SECRET_KEY, DEEPSEEK_API_KEY, DEBUG, ALLOWED_HOSTS.

### 3️⃣ Auto-deploy

Render builds and launches Gunicorn using:

```
web: bash ./start.sh
```

### 4️⃣ Visit your live URL

Your app works instantly on Render free tier.

---

## 🧩 Dependencies

```
Django
gunicorn
whitenoise
requests
pdfplumber
python-docx
openpyxl
python-dotenv
dj-database-url
```

---

## 🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first.

---

## 📜 License

This project is released under the **MIT License**.

---

## ❤️ Author

**Madhesh SR**


---

# ⭐ If you like this project, give it a star on GitHub!

```

---

If you want, I can also:

✅ Design a professional **project logo**  
✅ Create a **screenshots section** for README  
✅ Add **API documentation**  
✅ Make README more advanced with architecture diagrams  

Just tell me!
```
