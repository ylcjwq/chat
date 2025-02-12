from dotenv import load_dotenv
import os


def load_config():
    load_dotenv()
    config = {
        'question_url': os.getenv("CHAT_URL") + 'chat/completions',
        'use_token_url': os.getenv("CHAT_URL") + 'query/usage_details',
        'chat_api_key': os.getenv("CHAT_API_KEY"),
        'get_chat_url': os.getenv("GET_CHAT_URL"),
        'chat_api_key_ff': os.getenv("CHAT_API_KEY_FF"),
        'get_image_url': os.getenv("CHAT_URL") + 'images/generations',
    }
    return config
