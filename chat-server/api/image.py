from fastapi import HTTPException, Depends
import requests
import json
from pack.config import load_config
from pack.my_logging import setup_logging
from utils.auth import get_current_user

logging = setup_logging()
config = load_config()
chat_api_key_ff, get_image_url = config["chat_api_key_ff"], config["get_image_url"]


def get_image(question: dict, current_user: int = Depends(get_current_user)):
    try:
        headers = {
            "Authorization": f"Bearer {chat_api_key_ff}",
            "Content-Type": "application/json",
        }
        payload = json.dumps(
            {
                "prompt": f"{question['question']},请说中文",
                "n": 1,
                "model": "dall-e-3",
                "size": "1024x1024",
            }
        )
        logging.info(f"用户ID[{current_user.user_id}]生成图片指令: {question['question']}")
        print(get_image_url)
        response = requests.request(
            "POST", get_image_url, headers=headers, data=payload
        )

        # 检查响应状态码
        response.raise_for_status()
        logging.info(f"用户ID[{current_user.user_id}]问题回答: {response.json()}")

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        # 捕获HTTP错误
        logging.error(f"HTTP error occurred: {str(http_err)}")
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except requests.exceptions.RequestException as e:
        # 捕获请求相关的异常
        logging.error(f"RequestException occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 捕获其他所有异常
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
