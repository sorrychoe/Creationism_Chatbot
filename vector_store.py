import os

from api import tokens
from model.doc import ingest_txt_documents

if __name__ == "__main__":
    openai_api_key = os.environ.get('OPENAI_API_KEY')

    text_files = os.path.join(os.getcwd(), "data")
    db_path = os.path.join(os.getcwd(), "db")

    text_path = "./data/"

    ingest_txt_documents(text_path, db_path, openai_api_key)
