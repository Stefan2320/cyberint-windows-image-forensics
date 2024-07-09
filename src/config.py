import os
from dotenv import load_dotenv


load_dotenv()

def get_api_key():
    api_key = os.getenv('API_KEY')
    return api_key