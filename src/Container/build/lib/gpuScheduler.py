from src.error import ERROR
from src.setting import DataBase, settingENVRead

def GPUScheduler() -> int | None:
    """
    해당 함수는 개발환경 컨테이너에 할당할 GPU의 스케줄링 처리 함수이다.

    해당 함수를 사용하기 위해 필요한 변수는 없다.

    출력값은 **int**으로 출력된다.
    """
    try:
        gpuDevice = []

        if settingENVRead["GPU"]["Status"] == True:
            for gpuDevices in range(settingENVRead["GPU"]["List"]):
                DataBase.execute(
                    f"select `GPU` from `devContainer` WHERE `GPU` NOT NULL and `GPU` = {gpuDevices - 1};"
                )
                gpuDevice.append(len(DataBase.fetchall()))

            return gpuDevice.index(min(gpuDevice))

        return None

    except:
        ERROR.Logging()
        return None
