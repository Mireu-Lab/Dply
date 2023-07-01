from src.error import ERROR
from src.set import Setting_ENV, DataBase, SQL, DockerClient, time


def sqlWrite(self, status: bool) -> None:
    DataBase.execute(
        f"""insert into DevContainer (
            CreatedTimes,
            DevContainerType,
            DevContainerID,
            ProjectName,
            MakeAccount,
            Port,
            DevContainerStatus
        ) values (
            ?, ?, ?, ?, ?, ?, ?
        );""",
        (
            float(time()),
            "SSH",
            str(self.devContainerID),
            str(self.projectName),
            None,
            int(self.Port),
            bool(status),
        ),
    )

    if len(self.gpuSetting) != 0:
        pass

    SQL.commit()

    return None


def containerRemove(self) -> None:
    """
    Container Bulid중 Error나 시스템적 이슈가 발생시 컨테이너 삭제를 하기 위해 구성된 시스템입니다.

    """
    DockerClient.containers.get(self.devContainerID).stop()
    DockerClient.containers.get(self.devContainerID).remove()

    DockerClient.networks.get(self.projectNetworks).remove()

    DockerClient.volumes.get(self.projectVolumes).remove()

    return None


def sshBuild(self) -> dict:
    """
    해당 함수는 SSH Lab Container를 생성하기 위한 함수입니다.
    """

    status = False

    Tag = Setting_ENV["Container"]["SSH"]["Tag"].replace("0", self.containerOS)
    if len(self.gpuSetting) != 0:
        Tag = "gpu" + Tag

    try:
        self.devContainerID = DockerClient.containers.create(
            f"""{Setting_ENV["Container"]["SSH"]["URL"]}:{Tag}""",
            hostname=self.projectName,
            name=f"{self.containerOS}_{self.projectName}",
            ports={"8888/tcp": self.Port},
            environment={"PASSWORD": self.password},
            device_requests=self.gpuSetting,
            network=self.projectNetworks,
            volumes={self.projectVolumes: {"bind": "/workspace", "mode": "rw"}},
        ).short_id  # 컨테이너 ID 클래스 변수에 지정

        status = True  # 컨테이너 생성 성공시 변경
        DockerClient.containers.get(self.devContainerID).start()  # 컨테이너 최종 확인후 실행

    except:
        ERROR.Logging()
        containerRemove(self)
        status = False  # 컨테이너 생성 실패시 변경

    sqlWrite(self, status)  # SQL 개발 컨테이너 정보 입력

    return {"status": status, "port": self.Port}
