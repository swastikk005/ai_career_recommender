# test_env.py
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path(__file__).parent / ".env"
print("Looking for:", env_path)

load_dotenv(dotenv_path=env_path)

key = os.getenv("OPENROUTER_API_KEY")
print("Loaded key:", key)
