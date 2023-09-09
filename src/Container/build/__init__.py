from src.error import ERROR
from src.setting import DockerClient, settingENVRead
from src.set import time

from .lib.randomPort import randomPort
from .lib.gpuScheduler import GPUScheduler

from .databases import databaseBuild
from .jupyter import jupyterBuild
from .ssh import sshBuild

import docker


class Build:
    def __init__(
        self,
        projectName: str,
        containerOS: str,
        password: str = None,
        databaseContainer: list = None,
        processor: str = "CPU",
    ) -> None:
        """
        해당 함수는 클래스 변수를 지정하기 위해서 사용되는 함수이다.

        자세한 변수명은 아래와 같이 구성되어있다.

        | 변수명            | 타입 | 기본값 | 설명                                                         |
        | ----------------- | ---- | ------ | ------------------------------------------------------------ |
        | projectName       | str  | -      | Project Name 이다.                                          |
        | containerOS       | str  | -      | devContainer OS설정이다.                                   |
        | password          | str  | None   | DevContainer에서 사용할 password이다.                      |
        | databaseContainer | list | None   | 데이터베이스 할당 리스트이다.                              |
        | processorPlans    | int  | 0      | Container CPU,GPU,RAM,DISK 할당 Lv를 번호로 받아 처리 한다. |
        | processor         | str  | CPU    | Container 프로세서를 GPU, CPU 설정 한다.                   |
        """

        self.runTime = time()  # 요청 시간
        self.projectName = projectName  # 프로젝트 이름

        self.processorType = processor  # 개발환경 컨테이너 프로세서 설정에 대한 클래스 변수

        self.containerOS = containerOS  # 개발환경 컨테이너 운영체제에 대한 클래스 변수
        self.password = password  # 개발환경 컨테이너 계정 비밀번호 설정에 대한 클래스 변수

        self.port = randomPort()  # 개발환경 컨테이너 접속 포트 설정
        self.devContainerID = None  # 개발환경 컨테이너 ID
        self.gpuSetting = None  # 개발환경 컨테이너 GPU 할당 리스트
        self.gpuID = None  # 개발환경 컨테이너 GPU 할당값

        self.databaseContainer = databaseContainer  # 데이터베이스 설정 리스트

        """Projects Docker Container Network Setting ID"""
        self.projectNetworks = DockerClient.networks.create(
            f"Build_Management_{projectName}_{self.port}_network", driver="bridge"
        ).id

        """Projects Docker Container Volume Setting ID"""
        self.devContainerVolumes = DockerClient.volumes.create(
            f"Build_Management_{projectName}_{self.containerOS}_volume", driver="local"
        ).id

        """GPU 프로세서 할당 처리"""
        if self.processorType == "GPU" or self.processorType == "gpu":
            if settingENVRead["GPU"]["Status"] == True:
                self.gpuID = GPUScheduler()
                
                self.gpuSetting = [
                    docker.types.DeviceRequest(
                        device_ids=[str(self.gpuID)], capabilities=[["gpu"]]
                    )
                ]
            

    def ssh(self) -> dict:
        """
        devContainer SSH Build 함수

        해당 함수는 Return으로 dict으로 출력하며 Return으로 출력하는 값은 아래와 같다.

        ```
        {
            "status": bool,
            "port": int
        }
        ```
        """
        return sshBuild(self)

    def jupyter(self) -> dict:
        """
        devContainer Jupyter Build 함수

        해당 함수는 Return으로 dict으로 출력하며 Return으로 출력하는 값은 아래와 같다.

        ```
        {
            "status": bool,
            "port": int
        }
        ```
        """

        return jupyterBuild(self)

    def database(self) -> list:
        """
        devContainer Database Build 함수

        해당 함수는 Return으로 list으로 출력하며 Return으로 출력하는 값은 아래와 같다.

        ```
        [
            {"database": str, "status": bool}
        ]
        ```
        """

        return databaseBuild(self)
