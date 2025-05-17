# embedding.py

import pandas as pd
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer

DATA_FILE = 'data/flipkart_products.csv'
INDEX_FILE = 'data/faiss_index.index'
META_FILE = 'data/product_metadata.pkl'
MODEL_NAME = 'all-MiniLM-L6-v2'

def load_data():
    df = pd.read_csv(DATA_FILE)
    df = df.dropna(subset=['text'])
    return df

def generate_embeddings(texts, model):
    return model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

def save_index_and_metadata(index, metadata):
    faiss.write_index(index, INDEX_FILE)
    with open(META_FILE, 'wb') as f:
        pickle.dump(metadata, f)
    print(f"Saved index to {INDEX_FILE} and metadata to {META_FILE}")

def main():
    print("Loading product data...")
    df = load_data()

    print("Loading SentenceTransformer model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Generating embeddings...")
    embeddings = generate_embeddings(df['text'].tolist(), model)

    print("Creating FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    metadata = df[['ProductName', 'Current_Price', 'MRP', 'Proccessor', 'Ram', 'Storage']].to_dict(orient='records')

    os.makedirs('data', exist_ok=True)
    save_index_and_metadata(index, metadata)

if __name__ == "__main__":
    main()
