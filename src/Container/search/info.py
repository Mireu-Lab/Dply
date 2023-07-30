from src.setting import DataBase


def singleInformation(self) -> dict:
    """
    해당 함수는 단일 프로젝트 컨테이너 정보를 출력하는 함수이다.

    해당 함수는 self.projectName 변수에 데이터값이 들어왔을때 경우에 작동되는 함수이다.

    결과값으로는 dict으로 출력되며 출력값으로는 아래와 같이 출력된다.

    ```
    {
        "projectName": str,
        "createdTimes": float,
        "devContainer": {
            "type": str,
            "gpu": bool,
            "status": bool,
            "port": int,
        },
        "databaseContainers": {
            str: {
                "status": bool,
                "ip": str,
            }
        }
    }
    ```
    """

    projectInfo = DataBase.execute(
        f"""select
                `projectName`,
                `devContainerType`,
                `devContainerStatus`,
                `port`,
                `gpu`,
                `createdTimes`,
                `updateTimes`,
                `devContainerID`
            from `devContainer` where `projectName` = '{str(self.projectName)}';"""
    ).fetchall()  # 개발 환경 컨테이너 정보 SQL Read

    gpuStatus = True if type(projectInfo[0][4]) == int else False

    """For 문을 이용하여 프로젝트 데이터베이스 컨테이너 할당 정보 SQL Read"""
    databaseContainerInfo = {}
    for databaseInfo in DataBase.execute(
        f"""select
                `databaseType`,
                `databaseStatus`,
                `databaseIP`,
                `updateTimes`
            from `databaseContainer` where `devContainerID` = '{str(projectInfo[0][7])}';"""
    ).fetchall():
        databaseContainerInfo.update(
            {
                str(databaseInfo[0]): {  # 컨테이너 타입
                    "status": bool(databaseInfo[1]),  # 컨테이너 작동 상황
                    "ip": str(databaseInfo[2]),  # 컨테이너 내부 IP
                    "updatetime": float(databaseInfo[3]),
                }
            }
        )

    return {
        "projectName": str(projectInfo[0][0]),
        "createdTimes": float(projectInfo[0][5]),
        "devContainer": {
            "type": str(projectInfo[0][1]),
            "gpu": bool(gpuStatus),
            "status": bool(projectInfo[0][2]),
            "port": int(projectInfo[0][3]),
            "updateTime": int(projectInfo[0][6]),
        },
        "databaseContainers": dict(databaseContainerInfo),
    }


def multipleInformation() -> list:
    """
    해당 함수는 복수 프로젝트 컨테이너 정보를 출력하는 함수이다.

    결과값으로는 list[dict]으로 출력되며 출력값은 아래와 같이 출력된다.

    ```
    [
        {
            "projectName": str,
            "devContainer": {
                "Type": str,
                "status": bool,
                "port": int,
                "gpu": int,
                "createdTimes": float,
            },
            "databaseContainer": [
                str
            ],
        },
        ...
    ]
    ```
    """

    outList = []

    """1차 개발환경 컨테이너 For문"""
    for projectInfo in DataBase.execute(
        f"""select `projectName`, `devContainerType`, `devContainerStatus`, `port`, `gpu`, `createdTimes`, `devContainerID` from `devContainer`;"""
    ).fetchall():
        databaseTypeName = []  # 프로젝트 데이터 베이스 리스트 셋업

        gpuStatus = True if type(projectInfo[4]) == int else False  # GPU 할당 상황

        """2차 데이터베이스 컨테이너 For문"""
        for databaseInfo in DataBase.execute(
            f"""select `databaseType` from `databaseContainer` where `devContainerID` = '{str(projectInfo[6])}';"""
        ).fetchall():
            databaseTypeName.append(databaseInfo[0])  # 데이터베이스 타입명만 list에 추가

        outList.append(
            {
                "projectName": str(projectInfo[0]),
                "devContainer": {
                    "Type": str(projectInfo[1]),
                    "status": bool(projectInfo[2]),
                    "port": int(projectInfo[3]),
                    "gpu": bool(gpuStatus),
                    "createdTimes": float(projectInfo[5]),
                },
                "databaseContainer": databaseTypeName,
            }
        )

    return outList
