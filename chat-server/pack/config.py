from dotenv import load_dotenv
import os


def load_config():
    load_dotenv()
    get_chat_url = os.getenv("GET_CHAT_URL")   # 查询用量接口
    question_url = os.getenv("CHAT_URL") + 'chat/completions'
    use_token_url = os.getenv("CHAT_URL") + 'query/usage_details'
    chat_api_key = os.getenv("CHAT_API_KEY")    # 免费apiKey
    chat_api_key_ff = os.getenv("CHAT_API_KEY_FF")   # 付费apiKey
    return question_url, use_token_url, chat_api_key, get_chat_url, chat_api_key_ff  # 返回配置值
