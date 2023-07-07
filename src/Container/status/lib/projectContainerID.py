from src.set import DataBase


def projectContainerIDs(self) -> dict:
    projectContainerInfo = {"devContainer": {}, "databaseContainers": {}}

    devContainerInfo = DataBase.execute(
        f"""select `devContainerID`, `devContainerStatus` from `devContainer` where `projectName` = '{self.projectName}';"""
    ).fetchall()[0]

    projectContainerInfo["devContainer"].update(
        {devContainerInfo[0]: {"status": devContainerInfo[1]}}
    )

    databaseInfo = DataBase.execute(
        f"""select `databaseID`, `databaseType`, `databaseStatus` from `databaseContainer` where `devContainerID` = '{devContainerInfo[0]}';"""
    ).fetchall()

    if len(databaseInfo) > 0:
        for databaseID in databaseInfo:
            projectContainerInfo["databaseContainers"].update(
                {
                    str(databaseID[0]): {
                        "type": str(databaseID[1]),
                        "status": bool(databaseID[2]),
                    }
                }
            )

    return projectContainerInfo
