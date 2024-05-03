import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import requests
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量
load_dotenv()

app = FastAPI()
# 添加跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的跨域请求，也可以指定特定的来源
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)

history = []
# 替换为你的ChatGPT API URL
url = os.getenv("CHAT_URL")


@app.post("/stream")
async def forward_request(question: dict):
    print(question)
    history.append({"role": "user", "content": question["question"]})
    payload = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": history,
        "stream": True,
    })
    headers = {
        # 替换为你的ChatGPT API Key
        'Authorization': f'Bearer {os.getenv("CHAT_API_KEY")}',
        'Content-Type': 'application/json'
    }

    # 将请求转发给服务器
    response = requests.post(
        url, data=payload, headers=headers, timeout=60000, stream=True)

    def generate():
        # 处理并逐个将每个块转发给页面
        for chunk in response.iter_lines():
            mChunk = chunk.decode('utf-8')
            print(mChunk)
            yield mChunk

    # 使用 StreamingResponse 直接返回生成器对象
    return StreamingResponse(generate(), media_type="text/event-stream")
