from fastapi import HTTPException
import requests
from pack.config import load_config
from pack.my_logging import logging

config = load_config()
get_chat_url, chat_api_key_ff = config['get_chat_url'], config['chat_api_key_ff']

def get_chat_token():
    try:
        headers = {
            'Authorization': f'{chat_api_key_ff}',
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST", get_chat_url, headers=headers)

        # 检查响应状态码
        response.raise_for_status()
        logging.info(f"Received assistant: {response.json()}")

        # 获取原始响应数据
        raw_data = response.json()
        # 过滤掉 apiKey 字段
        filtered_data = {key: value for key,
                         value in raw_data.items() if key != 'apiKey'}
        return filtered_data

    except requests.exceptions.HTTPError as http_err:
        # 捕获HTTP错误
        logging.error(f"HTTP error occurred: {str(http_err)}")
        raise HTTPException(
            status_code=response.status_code, detail=str(http_err))
