from src.error import ERROR
from src.Container import (
    build as containerBuilder,
    delete as containerDelete,
    find as containerSearch,
)

from fastapi import FastAPI
from jsonset import buildOS, databaseBuild, buildType


api = FastAPI()


@api.post("/container/build", tags=["Container"])
async def containerBuild(
    projectName: str,
    containerType: buildType = "Jupyter",
    containerOS: buildOS = "ubuntu",
    databaseContainer: databaseBuild = None,
    password: str = None,
):
    devContainerBuilder = None
    try:
        ContainerBuilderClass = containerBuilder.Build(projectName, containerOS, password)

        if type(ContainerBuilderClass) == None:
            match containerType:
                case "Jupyter":
                    devContainerBuilder = ContainerBuilderClass.jupyter()
                    
                case "SSH":
                    devContainerBuilder = ContainerBuilderClass.ssh()

            return {
                "devContainer": {
                    "status": devContainerBuilder.status,
                    "port": devContainerBuilder.port,
                },
                "databaseContainer": ContainerBuilderClass.databaseBuild(databaseContainer),
            }

        else:
            return ContainerBuilderClass

    except:
        ERROR.Logging()
        return ERROR.API_Error_Messages(500)


@api.delete("/container/remove", tags=["Container"])
async def containerRemove(projectName: str):
    pass


@api.get("/container/find", tags=["Container"])
async def containerFind(search: str):
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(api, host="0.0.0.0", port=16170)
