# 🛍️ AI-Powered Laptop Assistant

SmartBuy is an AI-powered e-commerce assistant for laptops that provides:
- 🔍 Semantic search based on user queries.
- 💬 Conversational recommendations using LLMs via Groq API.
- 🎁 Similar product suggestions based on embeddings.
- 🕓 Search history logging via SQLite.

---

## 📦 Features

1. **Semantic Search** – Retrieve laptops based on user intent using sentence-transformer embeddings and FAISS.
2. **Chatbot Assistant** – Ask natural language queries and get AI-generated answers with product suggestions.
3. **Recommendation Engine** – Get similar laptop recommendations based on selected product.
4. **Recent Logs** – Displays recent search interactions stored in a local SQLite database.

---
## Run the App
bash
streamlit run app.py

---
## 🧠 Tech Stack

| Component       | Technology Used                                    |
| --------------- | -------------------------------------------------- |
| Backend         | Python                                             |
| Frontend        | Streamlit                                          |
| Vector Search   | FAISS                                              |
| Embeddings      | SentenceTransformers  ('all-MiniLM-L6-v2')         |
| LLM API         | Groq (supports llama3-8b-8192, gemma-7b-it, etc.)  |
| Database        | SQLite for search/chat logs                        |

---
## Project Structure

```
project
├── app.py                  # Streamlit frontend
├── db.py                   # SQLite logging utilities
├── embedding.py            # Embedding + FAISS index generator
├── process_data.py         # Cleans and prepares product data
├── rag_pipeline.py         # RAG pipeline with semantic search + chatbot
├── recommended.py          # Similar product recommender
├── data/
│   ├── raw/
│   │   └── Flipkart_laptops.csv  # Raw laptop data
│   ├── flipkart_products.csv     # Cleaned product data
│   ├── faiss_index.index         # FAISS vector index
│   └── product_metadata.pkl      # Metadata for indexed products
├── db.sqlite               # Local SQLite DB
└── .env                    # API Key (not committed)

```

---
## 📝 Notes
- Run process_data.py to clean raw laptop data.

- Then run embedding.py to generate embeddings and build the FAISS index.

- The app supports offline functionality for semantic search and recommendations.
Only the chatbot depends on internet access via the Groq API for LLM responses.



