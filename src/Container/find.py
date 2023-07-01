from src.error import ERROR
from src.set import Setting_ENV, SQL, DataBase
import random


def find(projectName: str = None) -> dict:
    Tag = ""

    if projectName != None:
        Tag = f"where DevContainerName = {projectName};"

    return dict(DataBase.execute(f"select * from DevContainer" + Tag).fetchall())


def containerNameCheck(projectName: str) -> bool:
    databaseReturn = DataBase.execute(
        f"""select exists (select * from `DevContainer` where `ProjectName` = '{projectName}');"""
    ).fetchall()[0][0]

    return bool(databaseReturn)
