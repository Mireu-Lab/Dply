from fastapi.responses import JSONResponse
from traceback import format_exc
from datetime import datetime
from json import load


Error_Code_Sample = load(open("Setting/Error.json", "r"))

class ERROR:
    def API_Error_Messages(
            StatusCode : int = 200, 
            MessagesType : str = None,
            Messages : str = None) -> (JSONResponse | None):

        """
        해당 함수는 FastAPI에 샘플 메시지나 따로 시스템 메시지를 전송할떄 사용됩니다.
        
        해당 함수를 사용하기 위해서 필요한 변수는 아래와 같다

        |변수명|데이터 타입|기본값|
        | --- | --- |--- |
        |StatusCode|int|200|
        |MessagesType|str|None|
        |Messages|str|None|
        으로 구성되어있다.

        해당 함수에 대해서 설명은 아래와 같다.

        - StatusCode : 에러코드를 전송하여 처리 해주는 코드이다.

        기초적으로 200, 202, 404, 403, 501, 503, 500으로 구성되어있다.
        
        또한 추가적으로 에러코드를 관리 하고 싶은경우 `SetData/Error.json`를 확인하여 추가 하시오.

        - MessagesType, Messages : 시스템 메시지 변수이다.
        
        기본값으로는 None으로 지정되어있으며 둘중에 하나라도 누락되는경우 시스템 에러를 출력한다.

        """
        ContentDict = {"msg" : Error_Code_Sample[str(StatusCode)]}

        try:
            if MessagesType:
                ContentDict.update({MessagesType : Messages})
                
        except TypeError:
            raise TypeError("Assignment variable missing")


        return JSONResponse(
            status_code=StatusCode, 
            content=ContentDict
        )


    def Program_Shutdown() -> None:
        #ErrorMessages : str = None
        """
        해당 함수는 비정상적인 상황이나 API 기술적 이슈가 발생되는경우 바로 셧다운을 하기 위해 구현된 API이다

        해당 함수를 사용하기 위해서 필요한 변수는 아래와 같다
        """
        
        print("Killed")
        exit()

    def Logging() -> None:
        logfile = open(f"Log/{datetime.now().__str__()}.log", "w+")
        
        logfile.write(format_exc())
        logfile.close()