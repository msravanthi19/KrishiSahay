import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_CSV = os.path.join(BASE_DIR, "clean_kcc.csv")
EMBED_DIR = os.path.join(BASE_DIR, "embeddings")

def run_milestone_2():
    print("🧠 Milestone 2: Generating Embeddings...")
    
    if not os.path.exists(CLEAN_CSV):
        print("❌ Error: clean_kcc.csv not found!")
        return

    df = pd.read_csv(CLEAN_CSV)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 1. Generate Embeddings
    embeddings = model.encode(df['Query'].tolist(), show_progress_bar=True)
    
    if not os.path.exists(EMBED_DIR):
        os.makedirs(EMBED_DIR)

    # 2. STORE AS kcc_embeddings.pkl (As per Milestone 2)
    with open(os.path.join(EMBED_DIR, "kcc_embeddings.pkl"), "wb") as f:
        pickle.dump(embeddings, f)
    
    # 3. Create FAISS Index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype('float32'))
    faiss.write_index(index, os.path.join(EMBED_DIR, "krishi_faiss.index"))
    
    # Metadata for Retrieval
    with open(os.path.join(EMBED_DIR, "meta.pkl"), "wb") as f:
        pickle.dump({'q': df['Query'].tolist(), 'a': df['Answer'].tolist()}, f)

    print("✅ Success: kcc_embeddings.pkl created in embeddings/ folder!")

if __name__ == "__main__":
    run_milestone_2()