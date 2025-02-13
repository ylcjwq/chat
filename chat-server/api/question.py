from fastapi import HTTPException, Depends
from fastapi.responses import StreamingResponse
import requests
import json
from pack.config import load_config
from pack.my_logging import setup_logging  # 导入日志记录器
from utils.auth import get_current_user

logging = setup_logging()

config = load_config()
# 从config获取的配置
[
    question_url,
    use_token_url,
    chat_api_key,
    get_chat_url,
    chat_api_key_ff,
    get_image_url,
] = list(config.values())

history = [
    {
        "role": "system",
        "content": "你的名字叫小金AI，你是一个问答机器人，你的开发者是袁隆成。",
    }
]


# 问答接口
async def forward_request(question: dict, current_user: int = Depends(get_current_user)):
    try:
        logging.info(f"用户ID[{current_user.user_id}]-问题：{question['question']}, 模型：{question['model']}")
        assistant_content = ""  # 用于存储最终内容的全局变量
        history.append({"role": "user", "content": question["question"]})
        payload = json.dumps(
            {
                "model": question["model"],
                "messages": history,
                "stream": True,
            }
        )
        if question["model"] == "gpt-3.5-turbo":
            key = chat_api_key
        else:
            key = chat_api_key_ff
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

        response = requests.post(
            question_url, data=payload, headers=headers, timeout=60000, stream=True
        )
        logging.info(f"用户ID[{current_user.user_id}]的提问回答完成。")

        def generate():
            nonlocal assistant_content  # 使用 nonlocal 关键字
            for chunk in response.iter_lines(chunk_size=10):
                if chunk:
                    try:
                        mChunk = chunk.decode("utf-8")
                        data = mChunk.split("data: ")[1]  # 直接分割并获取第二部分
                        if data.endswith("[DONE]"):
                            logging.info(f"用户ID[{current_user.user_id}]-回答为： {assistant_content}")
                            history.append(
                                {"role": "assistant", "content": assistant_content}
                            )
                            break
                        item = json.loads(data)
                        choices = item.get("choices", [])
                        if choices:
                            content = choices[0].get("delta", {}).get("content", "")
                            assistant_content += content
                            # 将内容作为生成器的一部分返回
                            yield "data: " + json.dumps(
                                {"content": content}, ensure_ascii=False
                            ) + "\n\n"
                    except Exception as e:
                        logging.error(f"RequestException occurred stream: {str(e)}")
                        yield "data: " + json.dumps(
                            {
                                "content": "服务器报错啦！！！，我也不知道啥原因，请联系袁隆成处理。"
                            },
                            ensure_ascii=False,
                        ) + "\n\n"
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
