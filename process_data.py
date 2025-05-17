import pandas as pd
import os

RAW_FILE = 'data/raw/Flipkart_laptops.csv'
PROCESSED_FILE = 'data/flipkart_products.csv'

def clean_text(val):
    if pd.isna(val):
        return ""
    return str(val).strip()

def process_flipkart_data():
    df = pd.read_csv(RAW_FILE)

    # Clean each column
    df['ProductName'] = df['ProductName'].apply(clean_text)
    df['Current_Price'] = df['Current_Price'].fillna(0).astype(float)
    df['MRP'] = df['MRP'].fillna(0).astype(float)
    df['Proccessor'] = df['Proccessor'].apply(clean_text)
    df['Ram'] = df['Ram'].apply(clean_text)
    df['Storage'] = df['Storage'].apply(clean_text)

    # Combine into a single text column for embedding
    df['text'] = df['ProductName'] + " | " + df['Proccessor'] + " | " + df['Ram'] + " RAM | " + df['Storage'] + " Storage"

    df.to_csv(PROCESSED_FILE, index=False)
    print(f"Processed data saved to: {PROCESSED_FILE}")

if __name__ == "__main__":
    process_flipkart_data()
