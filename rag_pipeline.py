import faiss
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer
from typing import List
import requests
import os
from db import log_interaction  # Add at top
from dotenv import load_dotenv
load_dotenv()

# CONFIG
INDEX_FILE = 'data/faiss_index.index'
META_FILE = 'data/product_metadata.pkl'
MODEL_NAME = 'all-MiniLM-L6-v2'
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # set this as env variable
GROQ_MODEL = "llama3-8b-8192"  # or gemma-7b-it, mixtral-8x7b

# Load embedding model
model = SentenceTransformer(MODEL_NAME)

def load_faiss_index():
    if not os.path.exists(INDEX_FILE) or not os.path.exists(META_FILE):
        raise FileNotFoundError("FAISS index or metadata not found. Please run embedding.py first.")
    
    index = faiss.read_index(INDEX_FILE)
    with open(META_FILE, 'rb') as f:
        metadata = pickle.load(f)
    return index, metadata

def semantic_search(query: str, k: int = 5) -> List[dict]:
    index, metadata = load_faiss_index()
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k)
    
    results = []
    for i in indices[0]:
        if i < len(metadata):
            results.append(metadata[i])
    return results

def format_results(results: List[dict]) -> str:
    response = ""
    for i, item in enumerate(results, start=1):
        response += (
            f"{i}. {item['ProductName']}\n"
            f"   - Price: ₹{item['Current_Price']}\n"
            f"   - MRP: ₹{item['MRP']}\n"
            f"   - Proccessor: {item['Proccessor']}\n"
            f"   - RAM: {item['Ram']}\n"
            f"   - Storage: {item['Storage']}\n\n"
        )
    return response.strip()

def query_llm_groq(prompt: str) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful e-commerce assistant. Help users choose the best products."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

from db import log_interaction  # Add at top

def chatbot_response(user_query: str) -> str:
    retrieved = semantic_search(user_query)
    if not retrieved:
        return "Sorry, I couldn't find any matching products."

    context = format_results(retrieved)
    prompt = f"""User asked: "{user_query}"

            Top matching laptop products:
            {context}

            Based on these, recommend the best options in a helpful and friendly way.
            """
    response = query_llm_groq(prompt)
    
    # Log to DB
    log_interaction("chatbot", user_query, response)

    return response


if __name__ == "__main__":
    user_input = input("Ask me something about laptops: ")
    response = chatbot_response(user_input)
    print("\n" + response)
