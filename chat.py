import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import requests

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
url = "https://api.chatanywhere.tech/v1/chat/completions"


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
        'Authorization': 'Bearer sk-OWTPo7uaer7h4dx1zZQ0JpitLWBVeexk5qOKTJGWQLsu9RPB',
        'Content-Type': 'application/json'
    }

    # 将请求转发给服务器 C
    response = requests.post(
        url, data=payload, headers=headers, timeout=60000, stream=True)

    def generate():
        # 将服务器 C 返回的 SSE 数据流传输给页面 A
        # 处理并逐个将每个块转发给页面 A
        for chunk in response.iter_lines():
            mChunk = chunk.decode('utf-8')
            print(mChunk)
            yield mChunk

    # 使用 StreamingResponse 直接返回生成器对象
    return StreamingResponse(generate(), media_type="text/event-stream")
