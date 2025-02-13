from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pack.config import load_config
from pack.my_logging import setup_logging
from api import api_router
from db import content

# 加载配置和环境变量
load_config()

# 设置日志
setup_logging()

# 初始化数据库连接池
content.initialize_connection_pool(
    {
        "host": "113.45.133.121",
        "user": "root",
        "password": "123456",
        "database": "ai_sql",
        "port": "3306",
    }
)

app = FastAPI()

# 添加跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router)
