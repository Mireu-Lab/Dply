from src.error import ERROR
from src.set import DataBase, SQL, DockerClient, time


def databaseVolume(self, projectVolumes: str, databaseType: str) -> None:
    """
    해당 함수는 데이터베이스 Save Volume설정을 하기 위한 함수이다.

    필요한 변수는 아래와 같다.

    |     변수명     | 타입 | 기본값 |       설명        |
    | :------------: | :--: | :----: | :---------------: |
    | projectVolumes | str  |   -    | Docker Volume ID  |
    |  databaseType  | str  |   -    | 데이터베이스 이름 |

    Return값은 None으로 출력된다.
    """
    if databaseType == "mysql":
        self.databaseSetting = [
            {"MYSQL_ROOT_PASSWORD": self.password},
            {projectVolumes: {"bind": "/var/lib/mysql", "mode": "rw"}},
        ]

    elif databaseType == "mariadb":
        self.databaseSetting = [
            {"MARIADB_ROOT_PASSWORD": self.password},
            {projectVolumes: {"bind": "/var/lib/maria", "mode": "rw"}},
        ]

    elif databaseType == "mongo":
        self.databaseSetting = [
            {
                "MONGO_INITDB_ROOT_USERNAME": "root",
                "MONGO_INITDB_ROOT_PASSWORD": self.password,
            },
            {projectVolumes: {"bind": "/data/db", "mode": "rw"}},
        ]

    elif databaseType == "redis":
        self.databaseSetting = [None, {projectVolumes: {"bind": "/data", "mode": "rw"}}]

    return None


def sqlWrite(
    self,
    databaseContainerID: str,
    databaseType: str,
    databaseContainerIP: str,
    Status: bool = False,
) -> None:
    """
    해당 함수는 databaseContainer Table에 insert를 하기 위한 함수이다.

    필요한 변수는 아래와 같다.

    |       변수명        | 타입 | 기본값 |                설명                |
    | :-----------------: | :--: | :------: | :--------------------------------: |
    | databaseContainerID | str  | -      |      데이터베이스 컨테이너 ID      |
    |    databaseType     | str  | -      |         데이터베이스 이름          |
    | databaseContainerIP | str  | -      |  데이터베이스 컨테이너 IP할당 값   |
    |       Status        | bool | False  | 데이터베이스 컨테이너 빌드 결과 값 |

    Return값은 None으로 출력된다.
    """
    DataBase.execute(
        """insert into `databaseContainer` (
            `devContainerID`,
            `databaseID`,
            `databaseType`,
            `databaseIP`,
            `databaseStatus`,
            `createdTimes`
        ) values (
            ?, ?, ?, ?, ?, ?
        );""",
        (
            str(self.devContainerID),
            str(databaseContainerID),
            str(databaseType),
            str(databaseContainerIP),
            bool(Status),
            float(time()),
        ),
    )

    SQL.commit()
    return None


def containerRemove(databaseContainerID: str) -> None:
    """
    해당 함수는 Container Bulid중 Error나 시스템적 이슈가 발생시 컨테이너 삭제를 하기 위해 구성된 시스템이다.

    필요한 변수는 아래와 같다.

    |       변수명        | 타입 | 기본값 |           설명           |
    | :-----------------: | :--: | :----: | :----------------------: |
    | databaseContainerID | str  |   -    | 데이터베이스 컨테이너 ID |

    Return값은 None으로 출력된다.
    """

    DockerClient.containers.get(databaseContainerID).stop()  # 컨테이너 정지
    DockerClient.containers.get(databaseContainerID).remove()  # 컨테이너 삭제

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
        databaseVolume(self, self.projectVolumes, databases)

        try:
            databaseContainerID = DockerClient.containers.create(
                databases + ":latest",  # 데이터베이스 컨테이너 이미지 파라미터
                hostname=f"""{databases}_{self.projectName}""",  # 데이터베이스 컨테이너 호스트 이름 파라미터
                name=f"{self.containerOS}_{databases}_{self.projectName}",  # 도커 컨테이너 이름 파라미터
                environment=self.databaseSetting[0],  # 데이터베이스 컨테이너 비밀번호 처리 파라미터
                network=self.projectNetworks,  # 도커 프로젝트 네트워크 할당 파라미터
                volumes=self.databaseSetting[1],  # 도커 프로젝트 볼륨 할당 파라미터
            ).short_id

        except:
            ERROR.Logging()
            containerRemove(databaseContainerID)  # 컨테이너 삭제

        try:
            DockerClient.containers.get(databaseContainerID).start()  # 컨테이너 실행

            # Database ContainerIP Check
            databaseContainerIP = DockerClient.containers.get(
                databaseContainerID
            ).attrs["NetworkSettings"]["Networks"][
                f"{self.projectName}_{self.port}_network"
            ][
                "IPAddress"
            ]

            status = True

        except:
            ERROR.Logging()
            status = False

        sqlWrite(
            self, databaseContainerID, databases, databaseContainerIP, status
        )  # SQL 데이터베이스 정보 입력

        databaseContainer_List.append(
            {"database": databases, "status": status}
        )  # 데이터베이스 구현 결과

    return databaseContainer_List
