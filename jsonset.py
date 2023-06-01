from pydantic import BaseModel
from enum import Enum


class buildOS(str, Enum):
    """debian, ubuntu, fedora, rockylinux"""
    debian = "debian"
    ubuntu = "ubuntu"
    fedora = "fedora"
    rockylinux = "rockylinux"

class databaseBuildList(str, Enum):
    """mysql, mariadb, mongodb, redis"""
    mysql = "mysql"
    mariadb = "mariadb"
    mongodb = "mongodb"
    redis = "redis"

class buildType(str, Enum):
    """SSH, Jupyter"""
    SSH = "SSH"
    Jupyter = "Jupyter"


class databaseBuild(BaseModel):
    databaseBuildList : list[databaseBuildList]