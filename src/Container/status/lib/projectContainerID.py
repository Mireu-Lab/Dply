from src.setting import DataBase


def projectContainerIDs(self) -> dict:
    """
    해당 함수는 프로젝트에서 할당된 컨테이너 ID를 Dict화 하기 위한 함수이다.

    해당 함수를 실행하기 위해 필요한 변수는 Class 변수를 호출하여 처리 하며 Return값은 Dict으로 출력된다.

    출력값으로는 아래와 같이 출력된다.

    ```
    {
        "devContainer": {
            str: {
                "status": bool
            }
        },
        "databaseContainers": {
            str: {
                "type": str,
                "status": bool
            }
        }
    }
    ```

    """

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
