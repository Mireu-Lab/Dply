from src.error import ERROR  # 자체 에러 관리용 Class

from json import load  # Setting ENV JSON 라이브러리
from dotenv import load_dotenv  # Setting .ENV File 라이브러리

import sqlite3, docker  # SQL, Docker SDK 라이브러리
import datetime

import torch

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


def GPUScheduler() -> int:
    """
    GPU 스케줄링 함수입니다.
    """

    try:
        gpuDevice = []

        for gpuDevices in torch.cuda.device_count():
            DataBase.execute(
                f"select GPU from DevContainer WHERE GPU IS NULL and GPU = {gpuDevices};"
            )
            gpuDevice.append(len(DataBase.fetchall()))

        return gpuDevice.index(min(gpuDevice))

    except:
        ERROR.Logging()
        return 0


def randomPort() -> int | None:
    """
    랜덤으로 포트 중복되지 않는 데이터를 출력합니다.
    """

    import random

    try:
        returnList = []

        # SQL Container Port Select
        DataBase.execute("select Port from DevContainer;")

        for row in DataBase.fetchall():
            returnList.append(row[0])

        # Random Num
        for _ in range(5):
            randomNum = random.randint(
                Setting_ENV["PortSet"]["MIN"], Setting_ENV["PortSet"]["MAX"]
            )

            returnInt = randomNum if randomNum not in returnList else None
            if returnInt != None:
                break

        return returnInt

    except:
        ERROR.Logging()
        return None


def time() -> float:
    return datetime.datetime.now().timestamp()
