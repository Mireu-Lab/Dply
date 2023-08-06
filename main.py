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
    """
    # Build

    The API is a program for deploying development environment containers.\
    The parameters required to use the API are as follows.

    |    Variable Name | Type | Default | Description |
    | :----------: | :--: | :-----: | :-------------------------------------------: |
    | projectName | str | - | Project Name |
    |  Processor | str | CPU | Processor Allocation Parameters |
    |      OS | str | Ubuntu | Development Environment Container Operating System Allocation Parameters |
    |     Type | str | Jupiter | Development Environment Container Access Method Allocation Parameters |
    |   Password | str | None | Project Distribution Container Password Allocation Parameters |
    | databaseList | list | None | Database Container Deployment Allocation Parameters |

    <br>

    The result is output as shown below.

    <br>

    The API also specifies the types that it supports.\
    The specified type is configured as follows.

    | Variable Name | Type | Support Type (Case Check) |
    | :------------: | :----: | :----------------------------: |
    | Processor    | str  | CPU, GPU                     |
    | OS           | str  | ubuntu, centos, rockylinux, tensorflow   |
    | Type         | str  | SSH, Jupyter                 |
    | databaseList | list | mysql, mariadb, mongo, redis |

    <br>

    You have to check the case and enter the college to avoid errors.\
    In addition, these character interpretations are implemented without a separate filter.

    ## Status Code

    ### Status Code 200

    The error was successfully distributed

    ```json
    {
        "devContainer": {
            "status": int,
            "port": int
        },
        "databaseContainer": [
            {
                "database": str,
                "status": bool
            },
            ...
        ]
    }
    ```


    ### Status Code 400

    The corresponding error may occur when the Docker Image is not Full.
    Run the installer again and process it.

    ```json
    {
        "msg": "You do not have permission.",
        "NotBuildContainer": "The name is already registered."
    }
    ```


    ### Status Code 503

    The error is an error that occurs when the project name is duplicated.
    Try again by changing the project name to another one.

    ```json
    {
        "msg": "You do not have permission.",
        "NotBuildContainer": "The name is already registered."
    }
    ```

    <br><br>

    ### Status Code 403

    This error is an error that occurs when the computing system attempts to assign an unprovided processor.

    ```json
    {
        "msg": "You do not have permission.",
        "SystemProcessorConfigurationError": "Your system does not support the processor you want. Please select a different processor."
    }
    ```
    """
    devContainerBuilder = None
    databaseContainers = None

    """프로젝트 이름 중복확인"""
    if containerSearch.containerNameCheck(buildInfo.projectName) == False:
        ContainerBuilderClass = containerBuilder.Build(
            buildInfo.projectName,
            buildInfo.OS,
            buildInfo.password,
            buildInfo.databaseList,
            buildInfo.Processor,
        )  # 컨테이너 빌드 파라미터 기본값

        # 시스템 GPU 확인
        if (buildInfo.Processor == "GPU" and ContainerBuilderClass.gpuID != None) or buildInfo.Processor == "CPU":
            # 컨테이너 접속 타입 빌드
            if buildInfo.Type == "Jupyter" or buildInfo.Type == "jupyter":
                devContainerBuilder = ContainerBuilderClass.jupyter()

            elif buildInfo.Type == "SSH" or buildInfo.Type == "ssh":
                devContainerBuilder = ContainerBuilderClass.ssh()

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
async def projectContainerStatus(projectName: str, statusSetting: statusSetting):
    """
    # Status

    This function is a program for managing the execution of project containers.\
    The parameters required to use the API are as follows.

    <br>

    |   Variable Name | Type | Default | Description |
    | :---------: | :--: | :----: | :-----------: |
    | projectName | str | - | Project Name |
    | statusSetting | str | - | Project Container Status Information |

    <br>

    The result is output as shown below.

    <br><br>

    ## Status Code
    ### Status Code 200

    ```json
    {
        "Status": {
            "devContainer": bool,
            "databaseContainer": {
                str: bool,
                ...
            }
        },
    }
    ```

    <br><br>

    ### Status Code 404

    ```json
    {
        "msg": "Not found",
        "NotFoundProjects": "Projects that cannot be found"
    }
    ```
    """
    if containerSearch.containerNameCheck(projectName) == True:
        return containerStatus.status(projectName, statusSetting).project()

    else:
        return ERROR.API_Error_Messages(
            404, "NotFoundProjects", "Projects that cannot be found"
        )  # 프로젝트 컨테이너가 없는경우


@api.delete("/container/remove", tags=["Container"])
async def containerRemove(projectName: str):
    """
    # Delete

    The API is a program for deleting development environment containers.

    The parameters required to use the API are as follows.

    |   Variable Name | Type | Default | Description |
    | :---------: | :--: | :----: | :-----------: |
    | projectName | str | - | Project Name |

    The result value is output as follows.

    <br><br>

    ## Status Code
    ### Status Code 200

    Project Delete Results

    ```json
    {
        "projectName": str,
        "projectStatus": {
            "devContainer": bool,
            "databaseContainers": {
                str: bool,
                ...
            },
            "containersNetwork": bool,
            "containersVolume": bool
        },
    }
    ```

    <br><br>

    ### Status Code 404

    If a project has already been deleted or is missing

    ```json
    {
        "msg": "Not found",
        "NotFoundProjects": "Projects that cannot be found"
    }
    """
    if containerSearch.containerNameCheck(projectName) == True:
        return containerDelete.remove(projectName).Project()  # 프로젝트 컨테이너 삭제

    else:
        return ERROR.API_Error_Messages(
            404, "NotFoundProjects", "Projects that cannot be found"
        )  # 프로젝트 컨테이너가 없는경우


@api.get("/container/find", tags=["Container"])
async def containerFind(projectName: str = None):
    """
    # Search

    The API is a program for deleting development environment containers.\
    The parameters required to use the API are as follows.

    |   Variable Name | Type | Default | Description |
    | :---------: | :--: | :----: | :-----------: |
    | projectName | str | None | Project Name |


    The function will also print **single project information** if the value 'projectName' is entered and **multiple project information** if not entered.

    The result is output as shown below.

    <br><br>

    ## Status Code

    ### Status Code 200
    #### Single Project Information

    ```json
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
            },
            ...
        }
    }
    ```

    <br>

    #### Multiple Project Information

    ```json
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
                str,
                ...
            ],
        },
        ...
    ]
    ```

    <br>

    #### No data from multiple project information

    ```json
    []
    ```


    ### Status Code 404

    Project information not found

    ```json
    {
        "msg": "Not found",
        "NotFoundProjects": "Projects that cannot be found"
    }
    ```
    """
    return containerSearch.Search(projectName).info()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(api, host="0.0.0.0", port=80)
