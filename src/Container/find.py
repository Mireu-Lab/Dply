from src.error import ERROR 
from src.set import Setting_ENV, SQL, DataBase
import random

def find():
    pass

def randomPort() -> (int | None):
    """
    랜덤으로 포트 중복되지 않는 데이터를 출력합니다.
    """
    try:
        returnList = []

        # SQL Container Port Select
        DataBase.execute("select Port from DevContainer;")

        for row in DataBase.fetchall():
            print(row)
            returnList.append(row)


        # Random Num
        for _ in range(5):
            randomNum = random.randint(
                Setting_ENV["PortSet"]["MIN"], 
                Setting_ENV["PortSet"]["MAX"])
            
            returnInt = randomNum if randomNum not in returnList else None
            if returnInt != None:
                pass

        return returnInt
                
    except: 
        ERROR.Logging()
        return None
