import mysql.connector
from mysql.connector import Error

# 全局变量，保存连接池对象
global_connection_pool = None


def initialize_connection_pool(config):
    """
    初始化数据库连接池
    :param config: 数据库配置
    """
    global global_connection_pool
    try:
        global_connection_pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name="ai_sql_pool", pool_size=5, **config
        )
        print("Connection pool created successfully")
    except Error as e:
        print(f"Error while creating connection pool: {e}")


def get_connection():
    """
    获取数据库连接
    """
    if global_connection_pool:
        try:
            connection = global_connection_pool.get_connection()
            if connection.is_connected():
                print("Successfully obtained a connection from the pool")
                return connection
        except Error as e:
            print(f"Error while getting connection from pool: {e}")
    return None


def release_connection(connection):
    """
    释放数据库连接
    """
    try:
        if connection and connection.is_connected():
            connection.close()
            print("Connection released back to the pool")
    except Error as e:
        print(f"Error while releasing connection: {e}")
