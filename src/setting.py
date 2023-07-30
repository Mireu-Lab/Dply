from src.error import ERROR  # 자체 에러 관리용 Class
from src.setting import GPUCheck, GPURange
from json import load, dump  # Setting ENV JSON 라이브러리

import sqlite3 # SQLSDK 라이브러리
import docker  # Docker SDK 라이브러리

settingENVRead = load(open("Setting/Setting.json", "r"))
settingENVWrite = open("Setting/Setting.json", "w")

# SQL Setup
print("SQL Check : ", end="")
try:
    SQL = sqlite3.connect(settingENVRead["SQL"])
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

# GPU Status
print("GPU Status : ", end="")
try:
    print(GPUCheck())
    
    settingENVRead["GPU"]["Status"] = GPUCheck()
    settingENVRead["GPU"]["List"] = GPURange()
    dump(settingENVRead, settingENVWrite, indent="\t")

except:
    pass