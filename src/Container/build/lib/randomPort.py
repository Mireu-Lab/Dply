from src.error import ERROR
from src.set import Setting_ENV, DataBase


def randomPort() -> int | None:
    """
    해당 함수는 Setting.json에서 할당한 최대값과 최소값을 이용하여 랜덤으로 포트 중복되지 않는 데이터를 출력하는 함수이다.

    해당 함수에서 필요한 변수는 없으며 출력값은 **int**나 **None**을 출력한다.

    **Int**는 정상적으로 port가 할당이 되는 값일때 출력되며 **None**일때는 할당할 포트가 없는경우 출력된다.
    """

    import random

    try:
        returnList = []

        # SQL Container port Select
        DataBase.execute("select `port` from `devContainer`;")

        for row in DataBase.fetchall():
            returnList.append(row[0])

        # Random Num
        for _ in range(5):
            randomNum = random.randint(
                Setting_ENV["portSet"]["MIN"], Setting_ENV["portSet"]["MAX"]
            )

            returnInt = randomNum if randomNum not in returnList else None
            if returnInt != None:
                break

        return returnInt

    except:
        ERROR.Logging()
        return None
