from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pack.my_logging import setup_logging

logging = setup_logging()


def clean_history():
    try:
        global history
        history = [
            {
                "role": "system",
                "content": "你的名字叫小金AI，你是一个问答机器人，你的开发者是袁隆成。",
            }
        ]
        return JSONResponse(
            status_code=200, content={"data": "历史记录已成功清除", "code": 200}
        )
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
