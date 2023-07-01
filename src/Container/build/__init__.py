from src.set import (
    DockerClient,
    GPUScheduler,
    randomPort,
)

from .databases import databaseBuild
from .jupyter import jupyterBuild
from .ssh import sshBuild

import docker


class Build:
    def __init__(
        self,
        processorPlans: int,
        processor: str,
        projectName: str,
        containerOS: str,
        password: str = None,
        databaseContainer: list = None,
    ) -> None:
        """
        해당 함수는 클래스 변수를 지정하기 위해서 사용되는 함수이다.

        자세한 변수명은 아래와 같이 구성되어있다.

        | 변수명            | 타입 | 기본값 | 설명                                                         |
        | ----------------- | ---- | ------ | ------------------------------------------------------------ |
        | processorPlans    | int  | -      | Container CPU,GPU,RAM,DISK 할당 Lv를 번호로 받아 처리 합니다. |
        | processor         | str  | CPU    | Container 프로세서를 GPU, CPU 설정 합니다.                   |
        | projectName       | str  | -      | Project Name입니다.                                          |
        | containerOS       | str  | -      | DevContainer OS설정입니다.                                   |
        | password          | str  | None   | DevContainer에서 사용할 password입니다.                      |
        | databaseContainer | list | None   | 데이터베이스 할당 리스트입니다.                              |
        """
        self.projectName = projectName  # 프로젝트 이름

        self.processorPlans = processorPlans  # 프로세서에 대한 플랜설정 클래스 변수
        self.processorType = processor  # 개발 컨테이너 프로세서 설정에 대한 클래스 변수

        self.containerOS = containerOS  # 개발 컨테이너 운영체제에 대한 클래스 변수
        self.password = password  # 개발 컨테이너 계정 비밀번호 설정에 대한 클래스 변수

        self.Port = randomPort()  # 개발 컨테이너 접속 포트 설정
        self.devContainerID = None  # 개발 컨테이너 ID
        self.gpuSetting = []  # 개발 컨테이너 GPU 할당 리스트

        self.databaseContainer = databaseContainer  # 데이터베이스 설정 리스트

        """Projects Docker Container Network Setting ID"""
        self.projectNetworks = DockerClient.networks.create(
            f"{projectName}_{self.Port}_network", driver="bridge"
        ).short_id

        """Projects Docker Container Volume Setting ID"""
        self.projectVolumes = DockerClient.volumes.create(
            f"{projectName}_{self.Port}_volume"
        ).short_id

        """GPU 프로세서 할당 처리"""
        if self.processorType == "GPU" or self.processorType == "gpu":
            self.gpuSetting = [
                docker.types.DeviceRequest(
                    device_ids=[GPUScheduler], capabilities=[["gpu"]]
                )
            ]

    def ssh(self) -> dict:
        """
        DevContainer SSH Build 함수

        해당 함수는 Return으로 dict으로 출력하며 Return으로 출력하는 값은 아래와 같다.

        `{"status": Bool, "port": Int}`
        """
        return sshBuild(self)

    def jupyter(self) -> dict:
        """
        DevContainer Jupyter Build 함수

        해당 함수는 Return으로 dict으로 출력하며 Return으로 출력하는 값은 아래와 같다.

        `{"status": Bool, "port": Int}`
        """

        return jupyterBuild(self)

    def database(self) -> list:
        """
        DevContainer Database Build 함수

        해당 함수는 Return으로 list으로 출력하며 Return으로 출력하는 값은 아래와 같다.

        `[  {"database": databases, "status": status}   ]`
        """

        return databaseBuild(self)
