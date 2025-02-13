import logging
import os
from datetime import datetime


def setup_logging():
    # 创建日志文件夹（如果不存在）
    log_dir = "log"
    os.makedirs(log_dir, exist_ok=True)

    # 创建一个 logger
    logger = logging.getLogger("app_logger")
    # 如果logger已经初始化过则直接返回
    if logger.hasHandlers():
        return logger
    logger.setLevel(logging.INFO)
    logger.propagate = False  # 阻止日志传播到父 logger

    # 获取当前日期，用于生成日志文件名
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_file_name = f"app.{current_date}.log"  # 日志文件名格式为 app.log.日期
    log_file_path = os.path.join(log_dir, log_file_name)  # 日志文件路径

    # 创建一个文件处理器，直接写入当天的日志文件
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # 创建一个控制台输出处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 设置日志格式
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器到 logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
