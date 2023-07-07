from src.error import ERROR  # 자체 에러 관리용 Class

from json import load  # Setting ENV JSON 라이브러리
from dotenv import load_dotenv  # Setting .ENV File 라이브러리

import sqlite3, docker  # SQL, Docker SDK 라이브러리
import datetime

Setting_ENV = load(open("Setting/Setting.json", "r"))
load_dotenv()

# SQL Setup
print("SQL Check : ", end="")
try:
    SQL = sqlite3.connect(Setting_ENV["SQL"])
    DataBase = SQL.cursor()

    print("Done!")

except:
    ERROR.Program_Shutdown()

# Docker Setup
print("Docker Check : ", end="")
try:
    DockerClient = docker.from_env()

    print("Done!")

except:
    ERROR.Program_Shutdown()


def time() -> float:
    return datetime.datetime.now().timestamp()
