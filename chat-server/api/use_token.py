from fastapi import HTTPException
import requests
import json
from pack.config import load_config
from pack.my_logging import logging

config = load_config()
use_token_url, chat_api_key = config['use_token_url'], config['chat_api_key']


def get_use_token():
    try:
        payload = json.dumps({
            "model": "%",
            "hours": 24
        })
        headers = {
            'Authorization': f'{chat_api_key}',
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST", use_token_url, headers=headers, data=payload)

        # 检查响应状态码
        response.raise_for_status()
        logging.info(f"Received assistant: {response.json()}")
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        # 捕获HTTP错误
        logging.error(f"HTTP error occurred: {str(http_err)}")
        raise HTTPException(
            status_code=response.status_code, detail=str(http_err))
    except requests.exceptions.RequestException as e:
        # 捕获请求相关的异常
        logging.error(f"RequestException occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 捕获其他所有异常
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
