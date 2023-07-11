from pydantic import BaseModel
from enum import Enum


class buildInfo(BaseModel):
    projectName: str  # 프로젝트 이름

    OS: str = "ubuntu"  # 개발환경 컨테이너 OS

    Type: str = "Jupyter"  # 개발환경 컨테이너 접속 방식
    password: str = None  # 개발환경 컨테이너 접속 비밀번호

    databaseList: list = None  # 프로젝트 데이터베이스 컨테이너 할당 리스트


class statusSetting(str, Enum):
    stop = "stop"
    start = "start"
    restart = "restart"
    kill = "kill"
