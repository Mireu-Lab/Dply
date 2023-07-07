from src.error import ERROR
from src.set import DockerClient

from .lib.sqlUpdate import commitDevContainer, commitDatabaseContainer


def devContainer(self) -> bool:
    status = bool(
        self.projectContainenrInfo["devContainer"][self.devContainerID]["status"]
    )

    if status == False:
        try:
            DockerClient.containers.get(self.devContainerID).start()
            status = True

        except:
            ERROR.Logging()
            status = False

    commitDevContainer(status, self.devContainerID, self.runTime)

    return status


def databaseContainer(self) -> dict:
    databaseContainerStatus = {}

    for containerID in self.databaseContainerID:
        status = bool(
            self.projectContainenrInfo["databaseContainers"][containerID]["status"]
        )

        if status == False:
            try:
                DockerClient.containers.get(containerID).start()
                status = True

            except:
                ERROR.Logging()
                status = False

        commitDatabaseContainer(
            status,
            self.devContainerID,
            self.projectContainenrInfo["databaseContainers"][containerID]["type"],
            self.runTime,
        )

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
