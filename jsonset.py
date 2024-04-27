from pydantic import BaseModel
from enum import Enum


class buildInfo(BaseModel):
    GitRepoURL: str  # Git Repo URL

    Processor: str = "CPU"  # 개발환경 컨테이너 할당 프로세서
    Image: str = "ubuntu"  # 개발환경 컨테이너 OS

    password: str = None  # 개발환경 컨테이너 접속 비밀번호

    databaseList: list = None  # 프로젝트 데이터베이스 컨테이너 할당 리스트


class statusSetting(str, Enum):
    stop = "stop"
    start = "start"
    restart = "restart"
    kill = "kill"
