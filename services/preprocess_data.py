import pandas as pd
import os
import json

# Paths setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "raw_kcc.csv")
CLEAN_CSV = os.path.join(BASE_DIR, "clean_kcc.csv")

def run_preprocess():
    print("🧹 Cleaning data...")
    if not os.path.exists(INPUT_FILE):
        print("❌ Error: raw_kcc.csv missing!")
        return

    df = pd.read_csv(INPUT_FILE)
    # Mapping columns
    df = df[['QueryText', 'KccAns']].dropna()
    df.rename(columns={'QueryText': 'Query', 'KccAns': 'Answer'}, inplace=True)
    
    # Save files
    df.head(1000).to_csv(CLEAN_CSV, index=False)
    print(f"✅ Clean data saved to {CLEAN_CSV}")

if __name__ == "__main__":
    run_preprocess()