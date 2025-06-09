
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

- ![image](https://github.com/user-attachments/assets/a30dc7a7-9f5c-4632-b68b-04a0812b3057)
 Landing Page
![image](https://github.com/user-attachments/assets/1098677a-9c54-4ca2-82ef-b8a736f0c308)
Chat UI
 ![image](https://github.com/user-attachments/assets/d28051bc-d987-441e-9554-d6c96e729993)
Admin Dashboard
- ![image](https://github.com/user-attachments/assets/13e78cf9-0a9a-43f4-890a-431f231c7255)
🎤Voice Recognition Integration
- ![image](https://github.com/user-attachments/assets/5766e63b-4175-47dd-ac35-36d76ff50f2b)
📑DocBot upload
![image](https://github.com/user-attachments/assets/14660b2c-5ca9-4679-af94-db254e7070e1)
interaction 

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

## 🙏 Acknowledgement

We thank our guide **Prof. Shree Gowri S S**, co-guide **Mr. Zameer Ahamed M Khan**, and the faculty of **KLS VDIT** for their constant guidance and encouragement.
