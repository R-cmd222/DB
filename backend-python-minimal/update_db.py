from models import engine
import os
from sqlalchemy import text

def update_database():
    # 读取SQL文件
    sql_file_path = os.path.join('..', 'SQL', 'update_bills_table.sql')
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')

    # 执行SQL命令
    with engine.connect() as connection:
        for command in sql_commands:
            command = command.strip()
            if command:  # 跳过空命令
                try:
                    print(f"执行SQL命令: {command}")
                    connection.execute(text(command))
                    connection.commit()
                    print("命令执行成功！")
                except Exception as e:
                    print(f"执行命令时出错: {str(e)}")
                    connection.rollback()

if __name__ == "__main__":
    update_database() 