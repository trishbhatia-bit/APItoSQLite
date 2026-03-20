import requests
import logging

def extract_from_api(url):
    logging.info(f"Extracting from {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Extraction failed: {e}")
        return []