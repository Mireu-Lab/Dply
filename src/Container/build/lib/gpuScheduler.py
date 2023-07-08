from src.error import ERROR
from src.set import DataBase

from dotenv import load_dotenv
from os import getenv

load_dotenv()

gpuSetting = int(getenv("GPUSetting"))  # 사용자 지정 GPU할당값


def GPUScheduler() -> int | None:
    """
    해당 함수는 개발환경 컨테이너에 할당할 GPU의 스케줄링 처리 함수이다.

    해당 함수를 사용하기 위해 필요한 변수는 없다.

    출력값은 **int**으로 출력된다.
    """
    try:
        gpuDevice = []

        if gpuSetting > 0:
            for gpuDevices in range(gpuSetting):
                DataBase.execute(
                    f"select `GPU` from `devContainer` WHERE `GPU` NOT NULL and `GPU` = {gpuDevices - 1};"
                )
                gpuDevice.append(len(DataBase.fetchall()))

            return gpuDevice.index(min(gpuDevice))

        return None

    except:
        ERROR.Logging()
        return None
