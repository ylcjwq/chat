from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pack.my_logging import setup_logging  # 导入日志记录器
from db import content
from mysql.connector import Error
import jwt
import datetime

logging = setup_logging()


async def login(login_data: dict):
    try:
        # 查询用户信息
        user_info = await query_user_from_db(login_data['user'], login_data['password'])

        if user_info:
            # 生成用户token
            token = generate_token(user_info["id"])
            logging.info(f"用户 {login_data['user']} 登录成功，用户ID: {user_info['id']}")
            return JSONResponse(content={"user_id": user_info["id"], "token": token})
        else:
            logging.warning(f"用户 {login_data['user']} 登录失败，用户名或密码错误")
            raise HTTPException(status_code=401, detail="用户名或密码错误")

    except HTTPException as e:
        logging.error(f"登录过程中发生错误: {str(e)}")
        raise

    except Exception as e:
        logging.error(f"登录过程中发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail="服务器内部错误")


# 查询匹配的用户信息
async def query_user_from_db(user, password):
    connection = content.get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            print(user, password)
            query = "SELECT * FROM users WHERE username = %s AND password_hash = %s;"
            cursor.execute(query, (user, password))
            result = cursor.fetchone()
            cursor.close()
            return result

        except Error as e:
            logging.error(f"Error while executing query: {e}")
            return None

        finally:
            content.release_connection(connection)
    return None


def generate_token(user_id):
    # 使用 JWT 生成 token
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24 * 30)
    }
    secret_key = "ylcjwq"  # 替换为你的密钥
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token
