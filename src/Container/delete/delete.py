from src.error import ERROR
from src.set import DataBase, DockerClient

import time


def sqlDelete(self) -> None:
    DataBase.execute(
        f"""delete from `DevContainer` where `DevContainerID` = '{self.DevContainerID}';"""
    )

    for databaseContainerID in self.databaseContainerID:
        DataBase.execute(
            f"""delete from `DatabaseContainer` where `DevContainerID` = '{databaseContainerID}';"""
        )

    return None


def projectDelete(self) -> dict:
    status = False

    try:
        DockerClient.containers.get(self.DevContainerID).stop()
        DockerClient.containers.get(self.DevContainerID).remove()

        for databaseContainerID in self.databaseContainerID:
            DockerClient.containers.get(databaseContainerID).stop()
            DockerClient.containers.get(databaseContainerID).remove()

        DockerClient.networks.get(self.projectNetworks).remove()
        time.sleep(2)
        DockerClient.volumes.get(self.projectVolumes).remove()

        sqlDelete(self)

        status = True

    except:
        ERROR.Logging()

    return {"projectName": self.projectName, "status": status}
