# 🤖 AI Chatbot Mentor  
### 🎓 Domain-Specific Intelligent Learning Assistant

AI Chatbot Mentor is a Streamlit-powered AI mentoring application designed for focused, structured, and domain-restricted learning.  
Unlike general-purpose chatbots, this mentor strictly responds only within the selected technical module, making it ideal for students, freshers, and guided self-learning environments.

---

## 🚀 Live Demo  
🔗 Streamlit App: (Add your deployed link here)

---

## ✨ Key Features

📚 Module-Based AI Mentoring  
🎯 Strict Domain Enforcement (No off-topic or hallucinated answers)  
🧠 Session-Based Conversation Memory  
💬 Interactive Chat Interface  
📥 Download full conversation as a `.txt` file  
🧼 Clean, minimal, beginner-friendly Streamlit UI  

---

## 📌 Available Learning Modules

- 🟢 Python  
- 🟣 SQL  
- 🔵 Power BI  
- 🟠 Exploratory Data Analysis (EDA)  
- 🟡 Machine Learning (ML)  
- 🔴 Deep Learning (DL)  
- 🟤 Generative AI (Gen AI)  
- ⚫ Agentic AI  

---

## 🧠 How It Works

1. User selects a learning module  
2. A module-specific system prompt is injected into the LLM  
3. The AI mentor:
   - ✅ Answers only questions related to the selected module  
   - ❌ Rejects unrelated questions with a fixed response  
4. Entire chat session is stored in memory  
5. User can download the full conversation anytime  

---

## ❌ Irrelevant Question Handling

If the user asks a question outside the selected module, the chatbot responds **exactly** with:

> **Sorry, I don’t know about this question. Please ask something related to the selected module.**

This ensures:
- 🔒 Domain accuracy  
- 🚫 Zero hallucinations  
- ✅ Reliable learning experience  

---

## 🧩 Tech Stack

| Component | Technology |
|---------|-----------|
| 🎨 Frontend | Streamlit |
| 🧠 LLM | Google Gemini |
| 🔗 AI Orchestration | LangChain |
| 🔐 Environment Variables | python-dotenv |
| 📄 File Export | Text (.txt) |

---

## 🎯 Use Cases

- 📘 Structured learning for beginners  
- 🎤 Interview preparation (module-wise)  
- 🏫 Classroom or training institute usage  
- 🤖 Domain-specific AI mentoring  
- 🛑 Avoiding misinformation from generic chatbots  

---

## 👨‍💻 Author

**Alok Mahadev Tungal**  
AI & Machine Learning Enthusiast | Generative AI Learner  
