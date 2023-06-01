from src.error import ERROR, JSONResponse
from src.set import Setting_ENV, DataBase, DockerClient

from src.Container.find import randomPort


def database(projectName: str, database: str) -> dict | None:
    if database == "mysql":
        return [(f"{projectName}_volume", "/var/lib/mysql")]

    elif database == "mariadb" or database == "maria":
        return [(f"{projectName}_volume", "/var/lib/maria")]

    elif database == "mongodb" or database == "mongo":
        return [(f"{projectName}_volume", "/data/db")]

    elif database == "redis":
        return [(f"{projectName}_volume", "/data")]

    else:
        return None


class Build:
    def __init__(
        self,
        projectName: str,
        containerOS: str,
        password: str = None,
        databaseContainer: list[str] = None,
    ) -> None:
        """
        해당 함수는 클래스 변수를 지정하기 위해서 사용되는 함수입니다.
        """

        self.projectName = projectName
        self.containerOS = containerOS
        self.password = password

        self.databaseContainer = databaseContainer

        self.projectNetworks = DockerClient.networks.create(
            f"{projectName}_network", driver="bridge"
        )

        self.projectVolumes = DockerClient.volumes.create(f"{projectName}_volume")

        self.Port = randomPort()

    @classmethod
    def ssh(self) -> dict | None:
        """
        해당 함수는 SSH Container를 생성하기 위한 함수입니다.
        """

        status = False

        try:
            DockerClient.containers.create(
                f"""{Setting_ENV["Container"]["SSH"]["URL"]}:{Setting_ENV["Container"]["SSH"]["Tag"].replace("0", self.containerOS)}""",
                hostname=self.projectName,
                name=f"{self.containerOS}_{self.projectName}",
                ports={"22/tcp": self.Port},
                network=None,
                volumes=[(self.projectVolumes, "/WorkSpace")],
            )

            status = True

        except:
            ERROR.Logging()

        return {"status": status, "port": None}

    @classmethod
    def jupyter(self) -> dict | None:
        """
        해당 함수는 Jupyter Lab Container를 생성하기 위한 함수입니다.
        """

        status = False

        try:
            DockerClient.containers.create(
                f"""{Setting_ENV["Container"]["Jupyter"]["URL"]}:{Setting_ENV["Container"]["Jupyter"]["Tag"].replace("0", self.containerOS)}""",
                hostname=self.projectName,
                name=f"{self.containerOS}_{self.projectName}",
                ports={"8888/tcp": self.Port},
                network=None,
                volumes=[(self.projectVolumes, "/WorkSpace")],
            )

            status = True

        except:
            ERROR.Logging()

        return {"status": status, "port": None}

    @classmethod
    def databaseBuild(self) -> dict | None:
        """
        해당 함수는 DB Container를 생성하기 위한 함수입니다.
        """

        databaseContainerList = []

        for databases in self.databaseContainer:
            try:
                DockerClient.containers.create(
                    databases,
                    hostname=self.projectName,
                    name=f"{self.containerOS}_{self.projectName}",
                    network=None,
                    volumes=database(self.projectName, databases),
                )

                status = True

            except:
                ERROR.Logging()
                status = False

            databaseContainerList.append({"database": database, "status": status})

        return databaseContainerList
