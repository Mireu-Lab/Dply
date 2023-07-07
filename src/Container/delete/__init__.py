from src.set import DataBase, DockerClient

from .delete import projectDelete


def containerIDFind(self, projectName: str) -> None:
    """
    해당 함수는 개발환경 컨테이너 ID와 데이터 베이스 컨테이너들 ID를 받아 클래스 변수로 지정 해주는 함수이다.

    해당 함수를 실행하기 위해서 필요한 변수는 아래와 같다.

    | 변수명 | 타입 | 기본값 |            설명            |
    | :----: | :--: | :----: | :--------------------: |
    | projectName | str |   None   | 프로젝트 이름 |

    결과값으로는 **None**이 출력된다.
    """

    devContainerInfo = DataBase.execute(
        f"SELECT `devContainerID`, `port` FROM `devContainer` WHERE `projectName` = '{projectName}'"
    ).fetchall()

    self.devContainerID = str(devContainerInfo[0][0])  # 개발환경 컨테이너 ID
    self.port = int(devContainerInfo[0][1])  # 개발환경 컨테이너 포트

    self.databaseContainerID = DataBase.execute(
        f"SELECT `databaseType`, `databaseID` FROM `databaseContainer` WHERE `devContainerID` = '{self.devContainerID}'"
    ).fetchall()  # 데이터베이스 컨테이너들 ID 리스트

    return None


class remove:
    def __init__(self, projectName: str = None) -> None:
        """
        해당 함수는 프로젝트 컨테이너를 삭제하기 위해 사용되는 Class이다.

        해당 함수에서 필요한 변수는 아래와 같다.

        | 변수명 | 타입 | 기본값 |            설명            |
        | :----: | :--: | :----: | :--------------------: |
        | projectName | str |   None   | 프로젝트 이름 |
        """

        self.projectName = projectName  # 프로젝트 이름

        self.devContainerID = None  # 개발 환경 컨테이너 ID
        self.port = None  # 개발 환경 컨테이너 포트

        self.databaseContainerID = []  # 프로젝트 데이터베이스 컨테이너 IDs

        containerIDFind(self, projectName)

        """Projects Docker Container Network Setting ID"""
        self.projectNetworks = DockerClient.networks.get(
            f"Build_Management_{projectName}_{self.port}_network"
        ).id

        """Projects Docker Container Volume Setting ID"""
        self.projectVolumes = set(
            containerID.id
            for containerID in DockerClient.volumes.list()
            if (containerID.id).startswith(
                f"Build_Management_{self.projectName}_{self.port}"
            )
        )

    def Project(self) -> dict:
        """
        해당 함수는 프로젝트 컨테이너를 최종적으로 삭제 하기 위한 함수이다.

        필요한 변수는 없으며 출력값으로는 dict으로 출력된다.

        출력 결과값은 아래와 같다.

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

        return projectDelete(self)
