from src.error import ERROR
from src.set import DockerClient

from .lib.sqlUpdate import commitDevContainer, commitDatabaseContainer


def devContainer(self) -> bool:
    status = bool(
        self.projectContainenrInfo["devContainer"][self.devContainerID]["status"]
    )

    if status == True:
        try:
            DockerClient.containers.get(self.devContainerID).stop()
            status = False

        except:
            ERROR.Logging()
            status = True

    commitDevContainer(status, self.devContainerID, self.runTime)

    return bool(status)


def databaseContainer(self) -> dict:
    databaseContainerStatus = {}

    for containerID in self.databaseContainerID:  # 데이터베이스 컨테이너 ID List
        status = bool(
            self.projectContainenrInfo["databaseContainers"][containerID]["status"]
        )

        if status == True:
            try:
                DockerClient.containers.get(containerID).stop()
                status = False

            except:
                ERROR.Logging()
                status = True

        commitDatabaseContainer(
            status,
            self.devContainerID,
            self.projectContainenrInfo["databaseContainers"][containerID]["type"],
            self.runTime,
        )
        status = False

        databaseContainerStatus.update(
            {
                self.projectContainenrInfo["databaseContainers"][containerID][
                    "type"
                ]: status
            }
        )

    return databaseContainerStatus


class containerStop:
    def single(self) -> dict:
        pass

    def multiple(self) -> dict:
        """
        해당 함수는 프로젝트 전체 컨테이너를 종료하는 함수이다.

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
