from dotenv import load_dotenv
import os


def load_config():
    load_dotenv()
    get_chat_url = os.getenv("GET_CHAT_URL")   # 查询用量接口
    question_url = os.getenv("CHAT_URL") + 'chat/completions'  # 问答接口
    use_token_url = os.getenv("CHAT_URL") + 'query/usage_details'  # 24小时用量查询
    get_image_url = os.getenv("CHAT_URL") + 'images/generations'  # 生成图片接口
    chat_api_key = os.getenv("CHAT_API_KEY")    # 免费apiKey
    chat_api_key_ff = os.getenv("CHAT_API_KEY_FF")   # 付费apiKey
    return question_url, use_token_url, chat_api_key, get_chat_url, chat_api_key_ff, get_image_url  # 返回配置值
