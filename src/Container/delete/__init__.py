from src.set import DataBase, DockerClient

from .delete import projectDelete


def containerIDFind(self, projectName: str) -> None:
    DevContainerInfo = DataBase.execute(
        f"SELECT `DevContainerID`, `Port` FROM `DevContainer` WHERE `DevContainerName` = '{projectName}'"
    ).fetchall()

    self.DevContainerID = str(DevContainerInfo[0][0])
    self.Port = int(DevContainerInfo[0][1])

    databaseContainerIDList = DataBase.execute(
        f"SELECT `DataBaseID` FROM `DatabaseContainer` WHERE `DevContainerID` = '{self.DevContainerID}'"
    ).fetchall()

    for databaseContainerID in databaseContainerIDList:
        self.databaseContainerID.append(databaseContainerID[0][0])

    return None


class remove:
    def __init__(self, projectName: str = None) -> None:
        self.projectName = projectName
        self.DevContainerID = None
        self.Port = 0
        self.databaseContainerID = []

        containerIDFind(self, projectName)

        """Projects Docker Container Network Setting ID"""
        self.projectNetworks = DockerClient.networks.get(
            f"{projectName}_{self.Port}_network"
        ).short_id

        """Projects Docker Container Volume Setting ID"""
        self.projectVolumes = DockerClient.volumes.get(
            f"{projectName}_{self.Port}_volume"
        ).short_id

    def Project(self) -> dict:
        return projectDelete(self)
