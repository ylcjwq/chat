from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .security import verify_token

# 创建一个 OAuth2 身份验证类
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class TokenData:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return str(self.user_id)


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
