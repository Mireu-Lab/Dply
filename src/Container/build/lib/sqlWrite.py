from src.error import ERROR
from src.set import DataBase, SQL


def devContainer(self, types: str, status: bool) -> None:
    """
    해당 함수는 databaseContainer Table에 insert를 하기 위한 함수이다.

    필요한 변수는 아래와 같다.

    | 변수명 | 타입 | 기본값 |            설명            |
    | :----: | :--: | :----: | :--------------------: |
    | status | bool |   -    | 개발환경 컨테이너 빌드 결과 |

    Return값은 None으로 출력된다.
    """

    DataBase.execute(
        f"""insert into `devContainer` (
            `projectName`,
            `devContainerID`,
            `devContainerType`,
            `devContainerStatus`,
            `port`,
            `makeAccount`,
            `createdTimes`,
            `updateTimes`
        ) values (
            ?, ?, ?, ?, ?, ?, ?, ?
        );""",
        (
            str(self.projectName),
            str(self.devContainerID),
            str(types),
            bool(status),
            int(self.port),
            None,
            float(self.runTime),
            float(self.runTime),
        ),
    )

    # GPU 할당값 업데이트
    if self.gpuSetting != None:
        DataBase.execute(
            f"""update devContainer set gpu = '{self.gpuID}' where devContainerID = '{self.devContainerID}';"""
        )

    SQL.commit()

    return None


def databaseContainer(
    self,
    databaseContainerID: str,
    databaseType: str,
    databaseContainerIP: str,
    Status: bool = False,
) -> None:
    """
    해당 함수는 databaseContainer Table에 insert를 하기 위한 함수이다.

    필요한 변수는 아래와 같다.

    |       변수명        | 타입 | 기본값 |                설명                |
    | :-----------------: | :--: | :------: | :--------------------------------: |
    | databaseContainerID | str  | -      |      데이터베이스 컨테이너 ID      |
    |    databaseType     | str  | -      |         데이터베이스 이름          |
    | databaseContainerIP | str  | -      |  데이터베이스 컨테이너 IP할당 값   |
    |       Status        | bool | False  | 데이터베이스 컨테이너 빌드 결과 값 |

    Return값은 None으로 출력된다.
    """
    DataBase.execute(
        """insert into `databaseContainer` (
            `devContainerID`,
            `databaseID`,
            `databaseType`,
            `databaseIP`,
            `databaseStatus`,
            `createdTimes`,
            `updateTimes`
        ) values (
            ?, ?, ?, ?, ?, ?, ?
        );""",
        (
            str(self.devContainerID),
            str(databaseContainerID),
            str(databaseType),
            str(databaseContainerIP),
            bool(Status),
            float(self.runTime),
            float(self.runTime),
        ),
    )

    SQL.commit()
    return None
