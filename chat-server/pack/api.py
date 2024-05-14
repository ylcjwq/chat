from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
import requests
import json
from pack.config import load_config
from pack.my_logging import logging  # 导入日志记录器

api_router = APIRouter()

# 从config获取的配置
question_url, use_token_url, chat_api_key, get_chat_url, chat_api_key_ff, get_image_url = load_config()

history = [{"role": "system", "content": "你的名字叫小金AI，你是一个问答机器人，你的开发者是袁隆成。"}]


@api_router.post("/stream")   # 问答接口
async def forward_request(question: dict):
    try:
        logging.info(
            f"Received question: {question['question'],question['model']}")
        assistant_content = ""  # 用于存储最终内容的全局变量
        history.append({"role": "user", "content": question["question"]})
        payload = json.dumps({
            "model": question['model'],
            "messages": history,
            "stream": True,
        })
        if question['model'] == "gpt-3.5-turbo":
            key = chat_api_key
        else:
            key = chat_api_key_ff
        headers = {
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json'
        }

        response = requests.post(
            question_url, data=payload, headers=headers, timeout=60000, stream=True)
        logging.info("Request to the API was successful.")

        def generate():
            nonlocal assistant_content  # 使用 nonlocal 关键字
            for chunk in response.iter_lines():
                if chunk:
                    try:
                        mChunk = chunk.decode('utf-8')
                        data = mChunk.split("data: ")[1]  # 直接分割并获取第二部分
                        if data.endswith("[DONE]"):
                            logging.info(
                                f"Received assistant: {assistant_content}")
                            history.append(
                                {"role": "assistant", "content": assistant_content})
                            break
                        item = json.loads(data)
                        choices = item.get("choices", [])
                        if choices:
                            content = choices[0].get(
                                "delta", {}).get("content", "")
                            assistant_content += content
                            # 将内容作为生成器的一部分返回
                            yield "data: " + json.dumps({"content": content}, ensure_ascii=False) + "\n\n"
                    except Exception as e:
                        logging.error(
                            f"RequestException occurred stream: {str(e)}")
                        yield "data: " + json.dumps({"content": "服务器报错啦！！！，我也不知道啥原因，请联系袁隆成处理。"}, ensure_ascii=False) + "\n\n"
                        return

        # 返回生成器
        return StreamingResponse(generate(), media_type="text/event-stream")

    except requests.exceptions.RequestException as e:
        # 捕获请求相关的异常
        logging.error(f"RequestException occurred: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 捕获其他所有异常
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/getUseToken")  # 获取24小时内使用量
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


@api_router.post("/getChatToken")  # 获取总使用量和剩余token量
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


@api_router.post("/cleanHistory")  # 清除历史记录
def clean_history():
    try:
        global history
        history = [
            {"role": "system", "content": "你的名字叫小金AI，你是一个问答机器人，你的开发者是袁隆成。"}]
        return JSONResponse(
            status_code=200,
            content={"data": "历史记录已成功清除", "code": 200}
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/getImage")  # 获取图片
def get_image(question: dict):
    try:
        headers = {
            'Authorization': f'Bearer {chat_api_key_ff}',
            'Content-Type': 'application/json'
        }
        payload = json.dumps({
            "prompt": f"{question['question']},请说中文",
            "n": 1,
            "model": "dall-e-3",
            "size": "1024x1024"
        })
        logging.info(f"生成图片指令: {question['question']}")
        print(get_image_url)
        response = requests.request(
            "POST", get_image_url, headers=headers, data=payload)

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
