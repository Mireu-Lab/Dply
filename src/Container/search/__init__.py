from typing import Any
from src.error import ERROR, JSONResponse
from src.set import DataBase

from .info import singleInformation, multipleInformation


class Search:
    def __init__(self, projectName: str = None) -> None:
        """
        해당 함수는 Class 변수를 지정하기 위한 함수이다.

        필요한 변수는 아래와 같다.

        | 변수명      | 타입 | 기본값 | 설명          |
        | ----------- | ---- | ------ | ------------- |
        | projectName | str  | None   | 프로젝트 이름 |
        """

        self.projectName = projectName

    def info(self) -> dict | JSONResponse:
        """
        해당 함수는 프로젝트 컨테이너의 정보를 출력하기 위한 함수이다.

        결과값으로는 dict나 JSONResponse를 출력하게 되며

        출력값으로는 아래와 같이 출력된다.


        - 단일 정보

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

        - 복수 정보

        데이터 있는경우
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

        - 복수 정보에서 데이터가 없는경우

        ```
        []
        ```


        - Status Code 404

        해당 결과값은 JSONResponse으로 출력된다.

        ```
        {
            "msg": "Not found",
            "NotFoundProjects": "Projects that cannot be found"
        }
        ```

        """
        if self.projectName != None:
            if containerNameCheck(self.projectName) == True:
                return singleInformation(self)

            else:
                return ERROR.API_Error_Messages(
                    404, "NotFoundProjects", "Projects that cannot be found"
                )

        else:
            return multipleInformation()


def containerNameCheck(projectName: str) -> bool:
    """
    해당 함수는 프로젝트 이름이 중복확인을 하기위한 함수이다.

    필요한 변수는 아래와 같다.

    | 변수명      | 타입 | 기본값 | 설명          |
    | ----------- | ---- | ------ | ------------- |
    | projectName | str  | None   | 프로젝트 이름 |

    결과값으로는 bool으로 출력된다.
    """

    databaseReturn = DataBase.execute(
        f"""select exists (select * from `devContainer` where `projectName` = '{projectName}');"""
    ).fetchall()[0][0]

    return bool(databaseReturn)
