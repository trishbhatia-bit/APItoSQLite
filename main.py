import logging
import os
import pandas as pd
from src.extractor import extract_from_api
from src.transformer import flatten_user, validate_records
from src.loader import load_to_sqlite, run_insights # New Imports

# Ensure folders exist
os.makedirs('data', exist_ok=True)
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("logs/pipeline.log"), logging.StreamHandler()]
)

def run_pipeline():
    url = "https://jsonplaceholder.typicode.com/users"
    
    # 1. Extract
    raw_data = extract_from_api(url)
    if not raw_data: return

    # 2. Transform
    flattened = [flatten_user(u) for u in raw_data]

    # 3. Validate
    valid, rejected = validate_records(flattened)

    # 4. Save CSVs
    if valid:
        pd.DataFrame(valid).to_csv('data/valid_users.csv', index=False)
        logging.info("Valid records saved to CSV.")
    
    if rejected:
        pd.DataFrame(rejected).to_csv('data/rejected_users.csv', index=False)
        logging.warning("Rejected records saved to CSV.")

    # 5. Load to SQLite (Phase 5)
    if valid:
        load_to_sqlite(valid)

    # 6. Run Insights (Phase 6)
    run_insights()

if __name__ == "__main__":
    run_pipeline()