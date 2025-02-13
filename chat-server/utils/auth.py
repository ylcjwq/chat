from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from .security import verify_token

# 创建一个 OAuth2 身份验证类
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class TokenData:
    user_id: int


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    获取当前用户
    :param token: 用户 Token
    :return: 用户 ID
    """
    try:
        user_id = verify_token(token)
        return TokenData(user_id=user_id)
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
            message=str(e),
        )
