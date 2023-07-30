from src.setting import time

from .lib.projectContainerID import projectContainerIDs

from .stop import containerStop
from .start import containerStart
from .restart import containerRestart
from .kill import containerKill


class status:
    def __init__(self, projectName: str, projectStatus: str) -> None:
        """
        해당 함수는 Class 변수를 지정하기 위한 함수이다.

        필요한 변수는 아래와 같다.

        | 변수명        | 타입 | 기본값 | 설명         |
        | :---------:   | :--: | :----: | :-----------: |
        | projectName   |  str | -  | 프로젝트 이름 |
        | projectStatus |  str | - | 사용자 요청 컨테이너 상태 파라미터 |
        """

        self.projectName = projectName  # 프로젝트 이름 파라미터
        self.projectStatus = projectStatus  # 사용자 요청 컨테이너 상태 파라미터

        self.runTime = time()  # 호출 시간 파라미터

        self.projectContainenrInfo = projectContainerIDs(self)  # 프로젝트 컨테이너 인적정보

        """개발환경 컨테이너 정보 리스트"""
        self.devContainerID = list(self.projectContainenrInfo["devContainer"])[0]

        """데이터베이스 컨테이너 정보 리스트"""
        self.databaseContainerID = list(
            self.projectContainenrInfo["databaseContainers"]
        )

    def project(self) -> dict:
        """
        해당 함수는 프로젝트 컨테이너 실행 관리를 위한 함수이다.

        결과값으로는 dict 출력하게 되며 출력값으로는 아래와 같이 출력된다.

        ```
        {
            "Status": {
                "devContainer": bool,
                "databaseContainer": {
                    str: bool
                }
            },
        }
        ```

        """
        match self.projectStatus:
            case "start":
                return containerStart.multiple(self)

            case "stop":
                return containerStop.multiple(self)

            case "restart":
                return containerRestart.multiple(self)

            case "kill":
                return containerKill.multiple(self)
