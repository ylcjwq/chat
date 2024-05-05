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


# @app.post("/stream")
# async def forward_request(question: dict):
#     print(question)
#     global assistant_content
#     assistant_content = ""
#     history.append({"role": "user", "content": question["question"]})
#     payload = json.dumps({
#         "model": "gpt-3.5-turbo",
#         "messages": history,
#         "stream": True,
#     })
#     headers = {
#         # 替换为你的ChatGPT API Key
#         'Authorization': f'Bearer {os.getenv("CHAT_API_KEY")}',
#         'Content-Type': 'application/json'
#     }

#     # 将请求转发给服务器
#     response = requests.post(
#         url, data=payload, headers=headers, timeout=60000, stream=True)

#     def generate():
#         global assistant_content
#         # 处理并逐个将每个块转发给页面
#         for chunk in response.iter_lines():
#             mChunk = chunk.decode('utf-8')
#             data = chunk.decode('utf-8').split("data: ")
#             for json_list in data[1:]:
#                 if json_list.endswith('[DONE]'):
#                     break
#                 item = json.loads(json_list.strip())
#                 choices = item.get("choices", [])
#                 if choices and choices[0] and 'finish_reason' in choices[0]:
#                     if choices[0]['finish_reason'] == 'stop':
#                         break
#                     content = choices[0].get("delta", {}).get("content", "")
#                     assistant_content += content
#                     yield mChunk

#     print(assistant_content)
#     # 使用 StreamingResponse 直接返回生成器对象
#     return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/stream")
async def forward_request(question: dict):
    print(question)
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
        url, data=payload, headers=headers, timeout=60000, stream=True)

    def generate():
        nonlocal assistant_content  # 使用 nonlocal 关键字
        for chunk in response.iter_lines():
            if chunk:
                try:
                    mChunk = chunk.decode('utf-8')
                    data = mChunk.split("data: ")[1]  # 直接分割并获取第二部分
                    if data.endswith("[DONE]"):
                        print('assistant', assistant_content)
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
                    print(e)
                    break

    # 返回生成器
    return StreamingResponse(generate(), media_type="text/event-stream")
