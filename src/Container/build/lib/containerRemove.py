from src.setting import DataBase, SQL, DockerClient

def devContainer(self) -> None:
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
            if (containerID.id).startswith(self.gitRepoURL):
                DockerClient.volumes.get(containerID.id).remove()
    except:
        pass

    return None


def dataabaseContainer(databaseContainerID: str) -> None:
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
