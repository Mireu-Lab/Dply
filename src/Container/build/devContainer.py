from src.error import ERROR
from src.setting import settingENVRead, DockerClient

from .lib.sqlWrite import devContainer as devContainer_sqlWrite
from .lib.containerRemove import devContainer as devContainer_remove

import docker


def devContainerBuild(self) -> dict:
    """
    해당 함수는 SSH Container를 생성하기 위한 함수입니다.

    해당 함수를 실행하기 위해 필요한 변수는 Class 변수를 호출하여 처리 하며 Return값은 Dict으로 출력된다.

    함수 결과값는 아래와 같이 출력된다.

    `{"status": int, "port": int}`
    """

    status = 500

    # GPU 프로세서 할당 시 이미지 변경
    if self.gpuSetting != None:
        Tag = "gpu" + Tag

    try:
        self.devContainerID = DockerClient.containers.create(
            f"""{self.gitRepo[2]}:latest""",  # 컨테이너 이미지 파라미터
            hostname=self.gitRepo[2],  # 컨테이너 할당 이름 파라미터
            name=self.gitRepo[2],  # 도커 컨테이너 이름 파라미터
            ports={"22/tcp": self.port},  # 컨테이너 Port 할당 파라미터
            environment={"PASSWORD": self.password},  # 컨테이너 기본 Password 파라미터
            device_requests=self.gpuSetting,  # GPU할당 파라미터
            network=self.projectNetworks,  # 프로젝트 컨테이너 네트워크 할당 파라미터
            volumes={
                f"./Projects/{self.gitRepo[2]}": {"bind": "/workspace", "mode": "rw"}
                "~/.ssh": {"bind": "/home/Hosting/.ssh", "mode": "ro"}
                "~/.gitconfig": {"bind": "/home/Hosting/.gitconfig", "mode": "rw"}
            },  # 프로젝트 컨테이너 볼륨 할당 파라미터
            restart_policy={"Name": "always"}
        ).short_id  # 컨테이너 ID 클래스 변수에 지정

        status = 200  # 컨테이너 생성 성공시 변경
        DockerClient.containers.get(self.devContainerID).start()  # 컨테이너 최종 확인후 실행

        devContainer_sqlWrite(self, "SSH", status)  # SQL 개발 컨테이너 정보 입력

    except docker.errors.ImageNotFound:
        devContainer_remove(self)  # 컨테이너 빌드 실패시 삭제
        status = 400  # 컨테이너 생성 실패시 변경

    except:
        ERROR.Logging()
        devContainer_remove(self)  # 컨테이너 빌드 실패시 삭제
        status = 500  # 컨테이너 생성 실패시 변경

    return {"status": status, "port": self.port}
