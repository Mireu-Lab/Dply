from src.Container.build import Build as containerBuilder
from src.error import ERROR
from src.Container import (
    build as containerBuilder,
    delete as containerDelete,
    find as containerSearch,
)

from fastapi import FastAPI
from jsonset import buildInfo


api = FastAPI()


@api.post("/container/build", tags=["Container"])
async def containerBuild(buildInfo: buildInfo, processorPlans: int = 0):
    devContainerBuilder = None
    databaseContainers = None

    if containerSearch.containerNameCheck(buildInfo.projectName) == False:
        ContainerBuilderClass = containerBuilder.Build(
            processorPlans,
            buildInfo.Processor,
            buildInfo.projectName,
            buildInfo.OS,
            buildInfo.Password,
            buildInfo.databaseList,
        )

        if buildInfo.Type == "Jupyter" or buildInfo.Type == "jupyter":
            devContainerBuilder = ContainerBuilderClass.jupyter()

        elif buildInfo.Type == "SSH" or buildInfo.Type == "ssh":
            devContainerBuilder = ContainerBuilderClass.ssh()

        if devContainerBuilder["status"] == True:
            if buildInfo.databaseList != None:
                databaseContainers = ContainerBuilderClass.database()

            return {
                "devContainer": {
                    "status": devContainerBuilder["status"],
                    "port": devContainerBuilder["port"],
                },
                "databaseContainer": databaseContainers,
            }

    else:
        return ERROR.API_Error_Messages(
            503, "NotBuildContainer", "The name is already registered."
        )


@api.put("/container/stop", tags=["Container"])
async def containerStop():
    pass


@api.put("/container/start", tags=["Container"])
async def containerRestart():
    pass


@api.put("/container/restart", tags=["Container"])
async def containerRestart():
    pass


@api.delete("/container/remove", tags=["Container"])
async def containerRemove(projectName: str):
    if containerSearch.containerNameCheck(projectName) == True:
        return containerDelete.remove(projectName).Project()

    else:
        return ERROR.API_Error_Messages(
            404, "NotFoundProjects", "Projects that cannot be found"
        )


@api.get("/container/find", tags=["Container"])
async def containerFind(search: str):
    pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(api, host="0.0.0.0", port=8080)
