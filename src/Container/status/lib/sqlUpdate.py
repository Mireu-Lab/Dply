from src.error import ERROR

from src.set import SQL, DataBase


def commitDevContainer(status: bool, ContainerID: str, times: float) -> None:
    DataBase.execute(
        f"""
        update 
            `devContainer` 
        set 
            `devContainerStatus` = {status}, `updateTimes` = {times} 
        where 
            `devContainerID` = '{ContainerID}';
        """
    )
    SQL.commit()
    return None


def commitDatabaseContainer(
    status: bool, ContainerID: str, ContainerType: str, times: float
) -> None:
    DataBase.execute(
        f"""
        update 
            `databaseContainer` 
        set 
            `databaseStatus` = {status}, `updateTimes` = {times} 
        where 
            `devContainerID` = '{ContainerID}' and `databaseType` = '{ContainerType}';"""
    )
    SQL.commit()

    return None
