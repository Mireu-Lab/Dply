from src.set import time

from .lib.projectContainerID import projectContainerIDs

from .stop import containerStop
from .start import containerStart
from .restart import containerRestart
from .kill import containerKill


class status:
    def __init__(self, projectName: str, projectStatus: str) -> None:
        self.projectName = projectName
        self.projectStatus = projectStatus

        self.runTime = time()

        self.projectContainenrInfo = projectContainerIDs(self)

        self.devContainerID = list(self.projectContainenrInfo["devContainer"])[0]
        self.databaseContainerID = list(
            self.projectContainenrInfo["databaseContainers"]
        )

    def project(self) -> dict:
        match self.projectStatus:
            case "start":
                return containerStart.multiple(self)

            case "stop":
                return containerStop.multiple(self)

            case "restart":
                return containerRestart.multiple(self)

            case "kill":
                return containerKill.multiple(self)
