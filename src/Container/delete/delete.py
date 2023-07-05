from src.error import ERROR
from src.set import DataBase, SQL, DockerClient


def devContainer(self) -> bool:
    """
    해당 함수는 개발환경 컨테이너를 삭제 하기 위한 함수이다.

    결과값으로는 Bool으로 출력된다.
    """

    Status = False

    try:
        """컨테이너 정지후 삭제"""
        DockerClient.containers.get(self.devContainerID).stop()
        DockerClient.containers.get(self.devContainerID).remove()

        """SQL 데이터 삭제"""
        DataBase.execute(
            f"""delete from `devContainer` where `devContainerID` = '{self.devContainerID}';"""
        )
        SQL.commit()

        Status = True

    except:
        ERROR.Logging()
        Status = False

    return Status


def databaseContainer(self) -> dict:
    """
    해당 함수는 데이터베이스 컨테이너를 삭제 하기 위한 함수이다.

    결과값으로는 dict[bool]으로 출력된다.

    출력 결과값으로는 아래와 같이 구성되어있다.

    ```
    {
        str: bool,
        ...
    }
    ```
    """

    databaseContainersStatus = {}

    for databaseContainerID in self.databaseContainerID:
        Status = False

        try:
            """컨테이너 정지후 삭제"""
            DockerClient.containers.get(databaseContainerID[1]).stop()
            DockerClient.containers.get(databaseContainerID[1]).remove()

            """SQL 데이터 삭제"""
            DataBase.execute(
                f"""delete from `databaseContainer` where `devContainerID` = '{self.devContainerID}';"""
            )
            SQL.commit()

            Status = True

        except:
            ERROR.Logging()
            Status = False

        databaseContainersStatus.update(
            {databaseContainerID[0]: Status}
        )  # 컨테이너 삭제 결과값 dict 추가

    return databaseContainersStatus


def projectVolume(self) -> bool:
    """
    해당 함수는 프로젝트 볼륨 삭제를 하기 위한 함수이다.

    결과값으로는 bool으로 출력된다.
    """

    Status = False

    try:
        """볼륨 이름이 프로젝트 이름과 같거나 겹치면 삭제"""
        for projectVolumes in self.projectVolumes:
            DockerClient.volumes.get(projectVolumes).remove()  # 볼륨 삭제

        Status = True

    except:
        ERROR.Logging()
        Status = False

    return Status


def projectNetwork(self):
    """
    해당 함수는 프로젝트 네트워크 삭제를 하기 위한 함수이다.

    결과값으로는 bool으로 출력된다.
    """

    Status = False

    try:
        DockerClient.networks.get(self.projectNetworks).remove()  # 네트워크 삭제
        Status = True

    except:
        ERROR.Logging()
        Status = False

    return Status


def projectDelete(self) -> dict:
    """
    해당 함수는 프로젝트 컨테이너, 볼륨, 네트워크를 삭제하는 함수이다.

    필요한 함수는 없으며 결과 타입은 dict이다.

    출력값은 아래와 같다.

    ```
    {
        "projectName": str,
        "projectStatus": {
            "devContainer": bool,
            "databaseContainers": dict[bool],
            "containersNetwork": bool,
            "containersVolume": bool
        },
    }
    ```
    """

    return {
        "projectName": self.projectName,
        "projectStatus": {
            "devContainer": devContainer(self),
            "databaseContainers": databaseContainer(self),
            "containersNetwork": projectNetwork(self),
            "containersVolume": projectVolume(self),
        },
    }
