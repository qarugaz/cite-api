import os
from dotenv import load_dotenv


load_dotenv()

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MISTRAL_API_KEY=os.getenv("MISTRAL_API_KEY")
GEMINI_MODEL=os.getenv("GEMINI_MODEL")
GEMINI_EMBEDDING_MODEL=os.getenv("GEMINI_EMBEDDING_MODEL")
GEMINI_MODEL_LITE=os.getenv("GEMINI_MODEL_LITE")
GEMINI_MODEL_1_5=os.getenv("GEMINI_MODEL_1_5")
DATABASE_URL=os.getenv("DATABASE_URL")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
QDRANT_URL = os.getenv("QDRANT_URL")
NEXT_URL = os.getenv("NEXT_URL")
LOG_DIR = os.getenv("LOG_DIR")