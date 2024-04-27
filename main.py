import src.setting
from src.error import ERROR
from src.Container import (
    build as containerBuilder,
    delete as containerDelete,
    search as containerSearch,
    status as containerStatus,
)

from fastapi import FastAPI
from jsonset import buildInfo, statusSetting


api = FastAPI()


@api.post("/container/build", tags=["Container"])
async def containerBuild(buildInfo: buildInfo):
    devContainerBuilder = None
    databaseContainers = None

    """프로젝트 이름 중복확인"""
    if containerSearch.containerNameCheck(buildInfo.gitRepoURL) == False:
        ContainerBuilderClass = containerBuilder.Build(
            buildInfo.GitRepoURL,
            buildInfo.Image,
            buildInfo.password,
            buildInfo.databaseList,
            buildInfo.Processor,
        )  # 컨테이너 빌드 파라미터 기본값

        # 시스템 GPU 확인
        if (buildInfo.Processor == "GPU" and ContainerBuilderClass.gpuID != None) or buildInfo.Processor == "CPU":
            # 컨테이너 접속 타입 빌드
            devContainerBuilder = ContainerBuilderClass.devContainer()
            
            if devContainerBuilder["status"] == 200:
                """데이터 베이스 컨테이너 빌드"""
                if buildInfo.databaseList != None:
                    databaseContainers = ContainerBuilderClass.database()

                return {
                    "devContainer": {
                        "status": devContainerBuilder["status"],
                        "port": devContainerBuilder["port"],
                    },
                    "databaseContainer": databaseContainers,
                }

            elif devContainerBuilder["status"] == 400:
                return ERROR.API_Error_Messages(
                    devContainerBuilder["status"],
                    "NoContainerImage",
                    "No container image required",
                )  # 개발환경 컨테이너 빌드 에러인경우
            
            else:
                return ERROR.API_Error_Messages(devContainerBuilder["status"])
            
        else:
            return ERROR.API_Error_Messages(
                403, 
                "SystemProcessorConfigurationError",
                "Your system does not support the processor you want. Please select a different processor."
            )
    else:
        return ERROR.API_Error_Messages(
            503, "NotBuildContainer", "The name is already registered."
        )  # 프로젝트 이름이 곂칠때 에러


@api.put("/project/container/status", tags=["Container"])
async def projectContainerStatus(gitRepoName: str, statusSetting: statusSetting):
    if containerSearch.containerNameCheck(gitRepoName) == True:
        return containerStatus.status(gitRepoName, statusSetting).project()

    else:
        return ERROR.API_Error_Messages(
            404, "NotFoundProjects", "Projects that cannot be found"
        )  # 프로젝트 컨테이너가 없는경우


@api.delete("/container/remove", tags=["Container"])
async def containerRemove(gitRepoURL: str):
    if containerSearch.containerNameCheck(gitRepoURL) == True:
        return containerDelete.remove(gitRepoURL).Project()  # 프로젝트 컨테이너 삭제

    else:
        return ERROR.API_Error_Messages(
            404, "NotFoundProjects", "Projects that cannot be found"
        )  # 프로젝트 컨테이너가 없는경우


@api.get("/container/find", tags=["Container"])
async def containerFind(gitRepoURL: str = None):
    return containerSearch.Search(gitRepoURL).info()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(api, host="0.0.0.0", port=8080)
