# 💻 AI-Powered Laptop Assistant

An interactive Streamlit-based chatbot that recommends laptops based on user queries using semantic search with FAISS and large language models (LLMs) from Cohere and Hugging Face.

---

## 🚀 Features

- Ask questions like:  
  *“Which laptop has long battery life and SSD?”*  
  *“Best laptops under ₹60,000 with i5 processor?”*
- Uses **FAISS** for semantic search
- Embedding via **HuggingFace** or **Cohere**
- LLM-powered responses using **Cohere Command models**
- Conversation memory for better contextual recommendations
- Saves search history to `Searching_history.json`

---

## 🧠 Tech Stack

| Component         | Tool/Library                      |
|------------------|------------------------------------|
| UI               | [Streamlit](https://streamlit.io)  |
| LLM              | Cohere via LangChain               |
| Embeddings       | HuggingFace SentenceTransformers   |
| Vector Store     | FAISS                              |
| Memory           | LangChain `ConversationBufferMemory` |
| Data             | Flipkart Laptop Dataset (CSV)      |
| Environment Vars | `python-dotenv`                    |

---

## 📁 Project Structure

project/
│
├── app.py # Streamlit app
├── Flipkart_laptops.csv # Laptop data for retrieval
├── Searching_history.json # Conversation history log
├── .env # Contains API keys
├── requirements.txt # All dependencies
└── README.md # You're here!
