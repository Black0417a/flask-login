import pymysql
from config import Config

def create_database():
    """确保MySQL数据库存在"""
    try:
        # 连接到MySQL服务器（不指定数据库）
        conn = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=int(Config.MYSQL_PORT)
        )
        
        cursor = conn.cursor()
        
        # 检查数据库是否存在
        cursor.execute(f"SHOW DATABASES LIKE '{Config.MYSQL_DB}'")
        result = cursor.fetchone()
        
        # 如果数据库不存在，则创建
        if not result:
            print(f"正在创建数据库: {Config.MYSQL_DB}")
            cursor.execute(f"CREATE DATABASE {Config.MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"数据库 {Config.MYSQL_DB} 创建成功")
        else:
            print(f"数据库 {Config.MYSQL_DB} 已存在")
        
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        print(f"创建数据库时发生错误: {e}")
        return False

if __name__ == "__main__":
    if create_database():
        print("你现在可以运行 'python init_db.py' 来初始化表和数据")
    else:
        print("无法创建数据库，请检查MySQL连接配置") 