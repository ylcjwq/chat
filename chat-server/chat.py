import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import requests
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

# 加载.env文件中的环境变量
load_dotenv()
# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=1024*1024*10,
                            backupCount=3, encoding='utf-8'),
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

app = FastAPI()
# 添加跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的跨域请求，也可以指定特定的来源
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)

history = [{"role": "system", "content": "你的名字叫小金AI，你是一个问答机器人，你的开发者是袁隆成。"}]
# 替换为你的ChatGPT API URL
question_url = os.getenv("CHAT_URL")+'chat/completions'    # 问答地址
use_token_url = os.getenv("CHAT_URL")+'query/usage_details'   # 计费地址


@app.post("/stream")  # 问答接口
async def forward_request(question: dict):
    try:
        logging.info(f"Received question: {question['question']}")
        assistant_content = ""  # 用于存储最终内容的全局变量
        history.append({"role": "user", "content": question["question"]})
        payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": history,
            "stream": True,
        })
        headers = {
            'Authorization': f'Bearer {os.getenv("CHAT_API_KEY")}',
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
                        logging.error(f"RequestException occurred: {str(e)}")
                        break

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


@app.post("/getUseToken")  # 获取24小时内使用量
def get_use_token():
    try:
        payload = json.dumps({
            "model": "%",
            "hours": 24
        })
        headers = {
            'Authorization': f'{os.getenv("CHAT_API_KEY")}',
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


@app.post("/getChatToken")  # 获取总使用量和剩余token量
def get_chat_token():
    try:
        headers = {
            'Authorization': f'{os.getenv("CHAT_API_KEY")}',
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "POST", os.getenv("GET_CHAT_URL"), headers=headers)

        # 检查响应状态码
        response.raise_for_status()
        logging.info(f"Received assistant: {response.json()}")
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        # 捕获HTTP错误
        logging.error(f"HTTP error occurred: {str(http_err)}")
        raise HTTPException(
            status_code=response.status_code, detail=str(http_err))
