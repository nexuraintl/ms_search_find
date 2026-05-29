import os
import aiomysql


MYSQL_HOST = os.getenv("DB1_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DATABASE = os.getenv("DB1_NAME")
MYSQL_USER = os.getenv("DB1_USER")
MYSQL_PASSWORD = os.getenv("DB1_PASS")


async def get_mysql_connection():

    connection = await aiomysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DATABASE,
        autocommit=True
    )

    return connection