from src.error import ERROR
from src.set import DataBase, SQL, DockerClient, time


def databaseVolume(projectVolumes: str, database: str) -> dict | None:
    if database == "mysql":
        return {projectVolumes: {"bind": "/var/lib/mysql", "mode": "rw"}}

    elif database == "mariadb":
        return {projectVolumes: {"bind": "/var/lib/maria", "mode": "rw"}}

    elif database == "mongo":
        return {projectVolumes: {"bind": "/data/db", "mode": "rw"}}

    elif database == "redis":
        return {projectVolumes: {"bind": "/data", "mode": "rw"}}

    else:
        return None


def sqlWrite(
    self,
    databaseContainerID: str,
    databaseType: str,
    databaseContainerIP: str,
    Status: bool = False,
) -> None:
    DataBase.execute(
        """insert into `DatabaseContainer` (
            `DevContainerID`,
            `DataBaseID`,
            `DataBaseType`,
            `DataBaseIP`,
            `DataBaseStatus`,
            `CreatedTimes`
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


def containerRemove(databaseContainerID) -> None:
    DockerClient.containers.get(databaseContainerID).stop()  # 컨테이너 정지
    DockerClient.containers.get(databaseContainerID).remove()  # 컨테이너 삭제

    return None


def databaseBuild(self) -> list:
    """
    해당 함수는 DB Container를 생성하기 위한 함수입니다.
    """

    databaseContainer_List = []

    for databases in self.databaseContainer:
        databaseContainer = None

        try:
            databaseContainer = DockerClient.containers.create(
                databases + ":latest",
                hostname=f"""{databases}_{self.projectName}""",
                name=f"{self.containerOS}_{databases}_{self.projectName}",
                network=self.projectNetworks,
                volumes=databaseVolume(self.projectVolumes, databases),
            ).short_id

        except:
            ERROR.Logging()
            containerRemove(databaseContainer)

        try:
            DockerClient.containers.get(databaseContainer).start()  # 컨테이너 실행

            databaseContainerIP = DockerClient.containers.get(databaseContainer).attrs[
                "NetworkSettings"
            ]["IPAddress"]
            status = True

        except:
            ERROR.Logging()
            status = False

        sqlWrite(
            self, databaseContainer, databases, databaseContainerIP, status
        )  # SQL 데이터베이스 정보 입력

        databaseContainer_List.append(
            {"database": databases, "status": status}
        )  # 데이터베이스 구현 결과

    return databaseContainer_List
