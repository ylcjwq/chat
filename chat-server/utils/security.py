import jwt
from fastapi import HTTPException

# 密钥和算法（建议从环境变量或配置文件中获取）
SECRET_KEY = "ylcjwq"
ALGORITHM = "HS256"


def verify_token(token: str):
    """
    校验 Token 的有效性
    :param token: 用户提供的 Token
    :return: 用户 ID
    """
    try:
        # 解码 Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise ValueError("Invalid token")
        return user_id
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(status_code=401, detail="Token expired") from e
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e
