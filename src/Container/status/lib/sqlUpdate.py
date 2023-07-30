from src.error import ERROR

from src.setting import SQL, DataBase


def commitDevContainer(status: bool, ContainerID: str, times: float) -> None:
    """
    해당 함수는 개발환경 컨테이너의 정보를 업데이트를 하기위한 함수이다.

    필요한 변수는 아래와 같이 구성되어있다.

    |   변수명    | 타입  | 기본값 |        설명         |
    | :---------: | :---: | :----: | :-----------------: |
    |   status    | bool  |   -    | 컨테이너 상태 정보  |
    | ContainerID |  str  |   -    |     컨테이너 ID     |
    |    times    | float |   -    | 함수 실행 요청 시간 |

    결과값으로는 None이 출력된다.
    """

    DataBase.execute(
        f"""
        update 
            `devContainer` 
        set 
            `devContainerStatus` = {status}, `updateTimes` = {times} 
        where 
            `devContainerID` = '{ContainerID}';
        """
    )
    SQL.commit()

    return None


def commitDatabaseContainer(
    status: bool, ContainerID: str, ContainerType: str, times: float
) -> None:
    """
    해당 함수는 데이터베이스 컨테이너의 정보를 업데이트 하기 위한 함수이다.

    필요한 변수는 아래와 같이 구성되어있다.

    |    변수명     | 타입  | 기본값 |        설명         |
    | :-----------: | :---: | :----: | :-----------------: |
    |    status     | bool  |   -    | 컨테이너 상태 정보  |
    |  ContainerID  |  str  |   -    |     컨테이너 ID     |
    | ContainerType |  str  |   -    |  데이터베이스 이름  |
    |     times     | float |   -    | 함수 실행 요청 시간 |

    결과값으로는 None이 출력된다.
    """

    DataBase.execute(
        f"""
        update 
            `databaseContainer` 
        set 
            `databaseStatus` = {status}, `updateTimes` = {times} 
        where 
            `devContainerID` = '{ContainerID}' and `databaseType` = '{ContainerType}';"""
    )
    SQL.commit()

    return None
