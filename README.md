
# 🎓 College InfoBot & DocBot

An **AI-powered chatbot system** designed for college websites to assist students, faculty, and visitors with real-time information and document-based queries using both voice and text input — exclusively in **English**.

---

## 🚀 Overview

**College InfoBot** is a smart, user-friendly assistant for the college website (e.g., KLS VDIT) that provides 24/7 help with college-related queries such as admissions, departments, events, and contact information. It uses real-time web scraping, semantic search (FAISS), and large language models (Cohere) to generate accurate, context-aware answers.

**DocBot**, a companion module, allows users to upload PDF/DOCX documents and query them using natural language. It utilizes vector embeddings (MiniLM + FAISS) and LLMs (Groq’s LLaMA3) to extract relevant responses from document content.

---

## 🧠 Features

- 🔎 AI-based semantic search and response generation
- 🗣️ Voice interaction support (Speech-to-Text & Text-to-Speech)
- 📚 DocBot for answering questions from uploaded documents
- 🧾 Admin dashboard for monitoring and feedback
- 📄 Web scraping with caching to avoid redundant requests
- 🔐 Secure session-based conversations and .env key handling

---

## 📌 Technologies Used

| Component           | Technology |
|---------------------|------------|
| Frontend            | HTML, CSS, JS, Web Speech API |
| Backend             | Python, Flask |
| NLP/LLM             | Cohere, Groq (LLaMA3), LangChain |
| Embeddings          | HuggingFace Transformers (MiniLM) |
| Vector Search       | FAISS |
| Web Scraping        | Selenium, BeautifulSoup |
| Document Parsing    | PyPDF2, python-docx |
| Voice APIs          | Google Speech-to-Text, gTTS |
| Session Management  | UUID, Flask-CORS |

---

## 🛠 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/ArunaVBhat/College-Infobot.git
   cd College-Infobot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** and add your API keys:
   ```
   COHERE_API_KEY=your_cohere_key
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_key
   GROQ_API_KEY=your_groq_key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

---


## 📷 Screenshots

- 🎯 ![Landing page](image.png)Landing Page, ![Chat with Infobot](image-1.png)Chat UI, ![Admin Dashboard](image-2.png)Admin Dashboard
- 🎤 ![Voice Recognition Integration](image-3.png)Voice Recognition Integration
- 📑 ![Uploading document](image-4.png)DocBot upload and ![Chat with Docbot](image-5.png)interaction examples

---
## ✨ Highlights

- **Single-language support**: optimized for English-only queries
- **Real-time answers**: powered by scraped data and LLMs
- **Document understanding**: ask questions from uploaded PDFs or DOCX
- **Role-based UI**: separate flows for students, staff, visitors, and admin
- **Feedback system**: collect user suggestions for improvements

---

## 📈 Future Enhancements

- Multilingual support (Kannada, Hindi)
- Integration with college ERP for personalized student/faculty data
- Sentiment detection and fallback improvements
- Mobile app with offline support
- Predictive notifications (deadlines, events)

---

## 👨‍💻 Authors

- Aruna Bhat 
- Deepshree Shintri
- N Chaitra
- Sakshi S Torgalmath

> Final Year CSE Students, KLS VDIT, Haliyal

---

## 📜 License

This project is licensed for academic and educational use only. For other uses, please contact the authors.

---

## 🙏 Acknowledgements

We thank our guide **Prof. Shree Gowri S S**, co-guide **Mr. Zameer Ahamed M Khan**, and the faculty of **KLS VDIT** for their constant guidance and encouragement.
