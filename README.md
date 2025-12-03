# 🔐 AntiGPT – AI Content Analyzer & Secure Chat System

AntiGPT is a Django-based web application that allows users to chat with an AI model running on an Ollama server.  
It includes user login/signup, admin management, conversation history, and AI response generation through your local or remote Ollama instance.

---

## 🚀 Features

- ✔️ User Registration & Login (Django Authentication)
- ✔️ Admin panel for managing users & messages
- ✔️ Chat system with conversation history
- ✔️ AI responses generated using **Ollama** models (e.g., Llama, Phi, Mistral)
- ✔️ Clean UI for chatting with the model
- ✔️ Fully deployable on Render (Frontend + Backend)
- ✔️ Secure environment variable handling (SECRET_KEY, DEBUG, ALLOWED_HOSTS)

---

## ⚠️ Important Before Login (Required Step)

If you are visiting the hosted website for the first time,  
you **must reset the admin username & password** before accessing the login page.

👉 **Reset Admin Credentials Here:**  
🔗 https://antigpt-v15z.onrender.com/reset-admin-password/

After resetting, go to the login page:

👉 **Login Page:**  
🔗 https://antigpt-v15z.onrender.com/login/

Use the username & password you set during the reset process.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 5, Python |
| Frontend | HTML, CSS, Django Templates |
| AI Engine | Ollama (Self-hosted LLMs) & DeepSeek LLM |
| Database | SQLite (local) / PostgreSQL (Render) |
| Deployment | Render Web Service |
| Static File Handling | Whitenoise |

---

## 🧩 How the System Works

- The user logs in and opens the chat interface.
- The chat history is saved in a Django model.
- When the user enters a message:
  - Django sends the message to an **Ollama Server API** (`/api/generate`).
  - Ollama returns the AI-generated reply.
  - The reply is saved and displayed in the UI.

---

## 🖥️ Running the Project Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Madhesh10/AntiGPT.git
cd AntiGPT
