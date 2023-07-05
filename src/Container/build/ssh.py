from src.error import ERROR
from src.set import Setting_ENV, DataBase, SQL, DockerClient, time

import docker


def sqlWrite(self, status: bool) -> None:
    """
    해당 함수는 databaseContainer Table에 insert를 하기 위한 함수이다.

    필요한 변수는 아래와 같다.

    | 변수명 | 타입 | 기본값 |            설명            |
    | :----: | :--: | :----: | :--------------------: |
    | status | bool |   -    | 개발환경 컨테이너 빌드 결과 |

    Return값은 None으로 출력된다.
    """
    DataBase.execute(
        f"""insert into devContainer (
            createdTimes,
            devContainerType,
            devContainerID,
            projectName,
            MakeAccount,
            port,
            devContainerStatus
        ) values (
            ?, ?, ?, ?, ?, ?, ?
        );""",
        (
            float(time()),
            "SSH",
            str(self.devContainerID),
            str(self.projectName),
            None,
            int(self.port),
            bool(status),
        ),
    )

    # GPU 할당값 업데이트
    if self.gpuSetting != None:
        DataBase.execute(
            f"""update devContainer set gpu = '{self.gpuID}' where devContainerID = '{self.devContainerID}';"""
        )

    SQL.commit()

    return None


def containerRemove(self) -> None:
    """
    해당 함수는 Container Bulid중 Error나 시스템적 이슈가 발생시 컨테이너 삭제를 하기 위해 구성된 시스템이다.

    해당 함수를 실행하기 위해 필요한 변수는 Class 변수를 호출하여 처리 하며 Return값은 None으로 출력된다.
    """
    try:
        # 개발 환경 컨테이너 정지후 삭제
        DockerClient.containers.get(self.devContainerID).stop()
        DockerClient.containers.get(self.devContainerID).remove()

        DataBase.execute(
            f"""delete from `devContainer` where `devContainerID` = '{self.devContainerID}';"""
        )
        SQL.commit()

    except:
        pass

    try:
        DockerClient.networks.get(self.projectNetworks).remove()  # 도커 컨테이너 네트워크 삭제

        # volume list중 프로젝트 name이있는 volume만 삭제
        for containerID in DockerClient.volumes.list():
            if (containerID.id).startswith(self.projectName):
                DockerClient.volumes.get(containerID.id).remove()
    except:
        pass

    return None


def sshBuild(self) -> dict:
    """
    해당 함수는 SSH Container를 생성하기 위한 함수입니다.

    해당 함수를 실행하기 위해 필요한 변수는 Class 변수를 호출하여 처리 하며 Return값은 Dict으로 출력된다.

    함수 결과값는 아래와 같이 출력된다.

    `{"status": int, "port": int}`
    """

    status = 500

    # 컨테이너 이미지 할당 값
    Tag = Setting_ENV["containerImageURL"]["SSH"]["TAG"].replace("0", self.containerOS)

    # GPU 프로세서 할당 시 이미지 변경
    if self.gpuSetting != None:
        Tag = "gpu" + Tag

    try:
        self.devContainerID = DockerClient.containers.create(
            f"""{Setting_ENV["containerImageURL"]["SSH"]["URL"]}:{Tag}""",  # 컨테이너 이미지 파라미터
            hostname=self.projectName,  # 컨테이너 할당 이름 파라미터
            name=f"{self.containerOS}_ssh_{self.projectName}",  # 도커 컨테이너 이름 파라미터
            ports={"22/tcp": self.port},  # 컨테이너 Port 할당 파라미터
            environment={"PASSWORD": self.password},  # 컨테이너 기본 Password 파라미터
            device_requests=self.gpuSetting,  # GPU할당 파라미터
            network=self.projectNetworks,  # 프로젝트 컨테이너 네트워크 할당 파라미터
            volumes={
                self.projectVolumes: {"bind": "/workspace", "mode": "rw"}
            },  # 프로젝트 컨테이너 볼륨 할당 파라미터
        ).short_id  # 컨테이너 ID 클래스 변수에 지정

        status = 200  # 컨테이너 생성 성공시 변경
        DockerClient.containers.get(self.devContainerID).start()  # 컨테이너 최종 확인후 실행

    except docker.errors.ImageNotFound:
        status = 400  # 컨테이너 생성 실패시 변경

    except:
        ERROR.Logging()
        containerRemove(self)  # 컨테이너 빌드 실패시 삭제
        status = 500  # 컨테이너 생성 실패시 변경

    sqlWrite(self, status)  # SQL 개발 컨테이너 정보 입력

    return {"status": status, "port": self.port}
