from pydantic import BaseModel
from enum import Enum

class buildInfo(BaseModel):
    projectName: str

    Processor: str = "CPU"
    OS: str = "ubuntu"

    Type: str = "Jupyter"
    Password: str = None

    databaseList: list = None