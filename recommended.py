# recommend.py

import faiss
import pickle
import pandas as pd
from sentence_transformers import SentenceTransformer
from typing import List
import os

# Paths and settings
INDEX_FILE = 'data/faiss_index.index'
META_FILE = 'data/product_metadata.pkl'
MODEL_NAME = 'all-MiniLM-L6-v2'

# Load SentenceTransformer model
model = SentenceTransformer(MODEL_NAME)

def load_data():
    if not os.path.exists(INDEX_FILE) or not os.path.exists(META_FILE):
        raise FileNotFoundError("Missing FAISS index or metadata file. Run embedding.py first.")

    index = faiss.read_index(INDEX_FILE)
    with open(META_FILE, 'rb') as f:
        metadata = pickle.load(f)
    
    return index, metadata

def recommend_similar_products(product_name: str, top_k: int = 5) -> List[dict]:
    index, metadata = load_data()

    # Create product lookup table
    df = pd.DataFrame(metadata)
    matched_row = df[df['ProductName'].str.lower() == product_name.lower()]

    if matched_row.empty:
        raise ValueError(f"No product found with name: {product_name}")
    
    # Use the same embedding logic as embedding.py
    text = (
        matched_row['ProductName'].values[0] + " | " +
        matched_row['Proccessor'].values[0] + " | " +
        matched_row['Ram'].values[0] + " RAM | " +
        matched_row['Storage'].values[0] + " Storage"
    )
    
    query_embedding = model.encode([text])
    distances, indices = index.search(query_embedding, top_k + 1)  # +1 to exclude self-match

    # Exclude the product itself from results
    original_index = matched_row.index[0]
    results = []
    for idx in indices[0]:
        if idx != original_index and idx < len(metadata):
            results.append(metadata[idx])

    return results[:top_k]

def display_recommendations(recommendations: List[dict]):
    print("Recommended Products:\n")
    for i, item in enumerate(recommendations, start=1):
        print(f"{i}. {item['ProductName']}")
        print(f"   - Price: ₹{item['Current_Price']}")
        print(f"   - Proccessor: {item['Proccessor']}")
        print(f"   - RAM: {item['Ram']}")
        print(f"   - Storage: {item['Storage']}")
        print()

if __name__ == "__main__":
    # Example usage
    query_product = input("Enter product name for recommendations: ")
    try:
        recs = recommend_similar_products(query_product, top_k=5)
        display_recommendations(recs)
    except ValueError as e:
        print(str(e))
