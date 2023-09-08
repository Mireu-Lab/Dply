from src.error import ERROR
from src.setting import DockerClient

from .lib.sqlWrite import databaseContainer as databaseContainer_sqlWrite
from .lib.containerRemove import dataabaseContainer as databaseContainer_remove


def databaseVolume(self, databaseType: str) -> None:
    """
    해당 함수는 데이터베이스 Save Volume설정을 하기 위한 함수이다.

    필요한 변수는 아래와 같다.

    |     변수명     | 타입 | 기본값 |       설명        |
    | :------------: | :--: | :----: | :---------------: |
    | projectVolumes | str  |   -    | Docker Volume ID  |
    |  databaseType  | str  |   -    | 데이터베이스 이름 |

    Return값은 None으로 출력된다.
    """

    databaseContainerVolumes = DockerClient.volumes.create(
        f"Build_Management_{self.projectName}_{databaseType}_volume",
        driver="local",
    ).id

    if databaseType == "mysql":
        self.databaseSetting = [
            {"MYSQL_ROOT_PASSWORD": self.password},
            {databaseContainerVolumes: {"bind": "/var/lib/mysql", "mode": "rw"}},
        ]

    elif databaseType == "mariadb":
        self.databaseSetting = [
            {"MARIADB_ROOT_PASSWORD": self.password},
            {databaseContainerVolumes: {"bind": "/var/lib/maria", "mode": "rw"}},
        ]

    elif databaseType == "mongo":
        self.databaseSetting = [
            {
                "MONGO_INITDB_ROOT_USERNAME": "root",
                "MONGO_INITDB_ROOT_PASSWORD": self.password,
            },
            {databaseContainerVolumes: {"bind": "/data/db", "mode": "rw"}},
        ]

    elif databaseType == "redis":
        self.databaseSetting = [
            None,
            {databaseContainerVolumes: {"bind": "/data", "mode": "rw"}},
        ]

    return None


def databaseBuild(self) -> list:
    """
    해당 함수는 DB Container를 생성하기 위한 함수이다.

    결과값은 아래와 같이 출력된다.

    `[ {"database": str, "status": bool}, ...]`
    """

    databaseContainer_List = []

    for databases in self.databaseContainer:
        databaseContainerID = None
        self.databaseSetting = None
        databaseVolume(self, databases)

        try:
            databaseContainerID = DockerClient.containers.create(
                databases + ":latest",  # 데이터베이스 컨테이너 이미지 파라미터
                hostname=f"""{databases}_{self.projectName}""",  # 데이터베이스 컨테이너 호스트 이름 파라미터
                name=f"Build_Management_{self.containerOS}_{databases}_{self.projectName}",  # 도커 컨테이너 이름 파라미터
                environment=self.databaseSetting[0],  # 데이터베이스 컨테이너 비밀번호 처리 파라미터
                network=self.projectNetworks,  # 도커 프로젝트 네트워크 할당 파라미터
                volumes=self.databaseSetting[1],  # 도커 프로젝트 볼륨 할당 파라미터
                restart_policy={"Name": "always"}
            ).short_id

        except:
            ERROR.Logging()
            databaseContainer_remove(databaseContainerID)  # 컨테이너 삭제

        try:
            DockerClient.containers.get(databaseContainerID).start()  # 컨테이너 실행

            # Database ContainerIP Check
            databaseContainerIP = DockerClient.containers.get(
                databaseContainerID
            ).attrs["NetworkSettings"]["Networks"][
                f"Build_Management_{self.projectName}_{self.port}_network"
            ][
                "IPAddress"
            ]

            status = True

        except:
            ERROR.Logging()
            status = False

        databaseContainer_sqlWrite(
            self, databaseContainerID, databases, databaseContainerIP, status
        )  # SQL 데이터베이스 정보 입력

        databaseContainer_List.append(
            {"database": databases, "status": status}
        )  # 데이터베이스 구현 결과

    return databaseContainer_List
