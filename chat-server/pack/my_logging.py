import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler('app.log', maxBytes=1024*1024*10,
                                backupCount=3, encoding='utf-8'),
            logging.StreamHandler()  # 控制台输出
        ]
    )
