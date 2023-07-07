from src.error import ERROR
from src.set import DockerClient

from .lib.sqlUpdate import commitDevContainer, commitDatabaseContainer


def devContainer(self) -> bool:
    """
    해당 함수는 개발환경 컨테이너를 실행시키기 위한 함수이다.

    결과값으로는 bool으로 출력되며 출력값으로는 아래와 같이 출력된다.

    - True: 컨테이너 실행

    - False: 컨테이너 종료
    """

    status = bool(
        self.projectContainenrInfo["devContainer"][self.devContainerID]["status"]
    )  # 기존 컨테이너 처리 상태

    if status == False:
        try:
            DockerClient.containers.get(self.devContainerID).start()  # 컨테이너 강제종료
            status = True

        except:
            ERROR.Logging()
            status = False

    commitDevContainer(status, self.devContainerID, self.runTime)  # SQL 처리

    return status


def databaseContainer(self) -> dict:
    """
    해당 함수는 데이터베이스 컨테이너를 실행시키기 위한 함수이다.

    결과값으로는 Dict[Bool]으로 출력되며 출력값으로는 아래와 같이 출력된다.

    ### 출력값

    ```
    {
        str: bool
    }
    ```

    ### Bool 처리값

    - True: 컨테이너 실행

    - False: 컨테이너 종료
    """

    databaseContainerStatus = {}

    for containerID in self.databaseContainerID:  # 데이터베이스 컨테이너 ID List
        status = bool(
            self.projectContainenrInfo["databaseContainers"][containerID]["status"]
        )  # 기존 컨테이너 처리 상태

        if status == False:
            try:
                DockerClient.containers.get(containerID).start()  # 컨테이너 강제종료
                status = True

            except:
                ERROR.Logging()
                status = False

        commitDatabaseContainer(
            status,
            self.devContainerID,
            self.projectContainenrInfo["databaseContainers"][containerID]["type"],
            self.runTime,
        )  # SQL 처리

        databaseContainerStatus.update(
            {
                self.projectContainenrInfo["databaseContainers"][containerID][
                    "type"
                ]: status
            }
        )

    return databaseContainerStatus


class containerStart:
    def single(self) -> dict:
        pass

    def multiple(self) -> dict:
        """
        해당 함수는 프로젝트 전체 컨테이너를 실행하는 함수이다.

        결과값으로는 dict으로 출력되며 출력값으로는 아래와 같이 출력된다.

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

        return {
            "Status": {
                "devContainer": devContainer(self),
                "databaseContainer": databaseContainer(self),
            },
        }
