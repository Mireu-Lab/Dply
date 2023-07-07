from src.error import ERROR
from src.set import DataBase

import torch


def GPUScheduler() -> int:
    """
    해당 함수는 개발환경 컨테이너에 할당할 GPU의 스케줄링 처리 함수이다.

    해당 함수를 사용하기 위해 필요한 변수는 없다.

    출력값은 **int**으로 출력된다.
    """
    try:
        gpuDevice = []

        for gpuDevices in range(torch.cuda.device_count()):
            DataBase.execute(
                f"select `GPU` from `devContainer` WHERE `GPU` NOT NULL and `GPU` = {gpuDevices - 1};"
            )
            gpuDevice.append(len(DataBase.fetchall()))

        return gpuDevice.index(min(gpuDevice))

    except:
        ERROR.Logging()
        return 0
